// Frida script per catturare la chiave/IV AES di SportzX a runtime.
// Uso:
//   frida -U -f com.sportzx.live -l sportzx_frida.js
// (serve un device/emulatore Android con ROOT + frida-server avviato, e USB debugging attivo)
//
// Cosa cattura:
//   1) javax.crypto.Cipher.init con AES  -> stampa KEY e IV in hex
//   2) export native di libadcb.so che contengono decrypt/crypt/aes/key/Cryptor
//      -> stampa i puntatori argomento e (se leggibili) i primi 32 byte dei buffer
//   3) creazione di String da byte[] che sembrano JSON decifrato (conferma)

function hex(b, n) {
    n = n || (b ? b.length : 0);
    if (!b) return '';
    var s = '';
    for (var i = 0; i < Math.min(n, b.length); i++) s += ('0' + (b[i] & 0xff).toString(16)).slice(-2);
    return s;
}

function tryRead(ptr, len) {
    try {
        if (ptr && !ptr.isNull()) return hex(ptr.readByteArray(len), len);
    } catch (e) {}
    return null;
}

function hookJavaCipher() {
    try {
        var Cipher = Java.use('javax.crypto.Cipher');
        function mk(ov) {
            ov.implementation = function (opmode, key, params) {
                try {
                    var alg = key.getAlgorithm();
                    if (alg && alg.indexOf('AES') >= 0) {
                        var iv = '';
                        try { if (params && params.getIV) iv = hex(params.getIV()); } catch (e) {}
                        console.log('[Cipher.init] op=' + opmode + ' alg=' + alg +
                                    ' KEY=' + hex(key.getEncoded()) + ' IV=' + iv);
                    }
                } catch (e) {}
                return ov.call(this, opmode, key, params);
            };
        }
        mk(Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec'));
        mk(Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec', 'java.security.SecureRandom'));
    } catch (e) { console.log('[!] Cipher non hookabile: ' + e); }
}

function hookString() {
    try {
        var String = Java.use('java.lang.String');
        var ov = String.$init.overload('[B', 'int', 'int', 'java.nio.charset.Charset');
        ov.implementation = function (data, off, len, cs) {
            var ret = ov.call(this, data, off, len, cs);
            try {
                var s = ret.toString();
                if (s.indexOf('eventInfo') >= 0 || (s.indexOf('"title"') >= 0 && s.indexOf('channels') >= 0)) {
                    console.log('[DECRYPTED JSON len=' + s.length + '] ' + s.slice(0, 400));
                }
            } catch (e) {}
            return ret;
        };
    } catch (e) { console.log('[!] String non hookabile: ' + e); }
}

function hookNativeLib() {
    var mod = Process.findModuleByName('libadcb.so') || Process.findModuleByName('libabcd.so');
    if (!mod) { console.log('[ ] libadcb.so non ancora caricata'); return; }
    console.log('[*] Modulo ' + mod.name + ' @ ' + mod.base);
    var targets = ['decrypt', 'Decrypt', 'crypt', 'Crypt', 'AES', 'aes', 'key', 'Key', 'Cryptor', 'cryptor'];
    var exports = mod.enumerateExports();
    exports.forEach(function (ex) {
        var name = ex.name || '';
        var hit = targets.some(function (t) { return name.indexOf(t) >= 0; });
        if (!hit) return;
        try {
            Interceptor.attach(ex.address, {
                onEnter: function (args) {
                    var parts = [name + '('];
                    for (var i = 0; i < 8; i++) {
                        var p = args[i];
                        if (!p) break;
                        var buf = tryRead(p, 32);
                        if (buf) parts.push('@' + i + '=0x' + p.toString() + '[' + buf + ']');
                        else parts.push('@' + i + '=0x' + p.toString());
                    }
                    parts.push(')');
                    console.log('[NATIVE] ' + parts.join(' '));
                }
            });
            console.log('[+] hook ' + name);
        } catch (e) { console.log('[!] hook ' + name + ' fallito: ' + e); }
    });
}

Java.perform(function () {
    hookJavaCipher();
    hookString();
});

// hook nativo subito e anche quando il modulo viene caricato
hookNativeLib();
try {
    Process.enumerateModules().forEach(function (m) {
        if (m.name === 'libadcb.so' || m.name === 'libabcd.so') hookNativeLib();
    });
} catch (e) {}
console.log('[*] Pronto. Apri Eventi nell\'app e guarda i log.');
