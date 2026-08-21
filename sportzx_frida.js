// Frida script per catturare la chiave/IV AES di SportzX a runtime.
// Uso: frida -U -f com.sportzx.live -l sportzx_frida.js
// (o su emulatore: frida -e -f com.sportzx.live -l sportzx_frida.js)
// Apri l'app, vai su Eventi: verranno stampate le chiavi AES in hex.
// Copia key e iv nelle impostazioni del addon (szx_key / szx_iv, formato hex).

function hex(b) {
    if (!b) return '';
    var s = '';
    for (var i = 0; i < b.length; i++) s += ('0' + (b[i] & 0xff).toString(16)).slice(-2);
    return s;
}

function tryHook(javaClass, hookFn) {
    try { var c = Java.use(javaClass); hookFn(c); }
    catch (e) { console.log('[!] ' + javaClass + ' non disponibile: ' + e); }
}

Java.perform(function () {
    // 1) Cattura init di javax.crypto.Cipher (utile se parte della crypto e' in Java)
    tryHook('javax.crypto.Cipher', function (Cipher) {
        var ov1 = Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec');
        ov1.implementation = function (opmode, key, params) {
            try {
                var alg = key.getAlgorithm();
                if (alg && alg.indexOf('AES') >= 0) {
                    var iv = '';
                    try { if (params && params.getIV) iv = hex(params.getIV()); } catch (e) {}
                    console.log('[Cipher.init] op=' + opmode + ' alg=' + alg + ' KEY=' + hex(key.getEncoded()) + ' IV=' + iv);
                }
            } catch (e) {}
            return ov1.call(this, opmode, key, params);
        };
        var ov2 = Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec', 'java.security.SecureRandom');
        ov2.implementation = function (opmode, key, params, sr) {
            try {
                var alg = key.getAlgorithm();
                if (alg && alg.indexOf('AES') >= 0) {
                    var iv = '';
                    try { if (params && params.getIV) iv = hex(params.getIV()); } catch (e) {}
                    console.log('[Cipher.init] op=' + opmode + ' alg=' + alg + ' KEY=' + hex(key.getEncoded()) + ' IV=' + iv);
                }
            } catch (e) {}
            return ov2.call(this, opmode, key, params, sr);
        };
    });

    // 2) Fallback: intercetta la creazione di String da byte[] che sembrano JSON decifrato
    tryHook('java.lang.String', function (String) {
        var ov = String.$init.overload('[B', 'int', 'int', 'java.nio.charset.Charset');
        ov.implementation = function (data, off, len, cs) {
            var ret = ov.call(this, data, off, len, cs);
            try {
                var s = ret.toString();
                if (s.indexOf('eventInfo') >= 0 || (s.indexOf('"title"') >= 0 && s.indexOf('channels') >= 0)) {
                    console.log('[DECRYPTED JSON len=' + s.length + '] ' + s.slice(0, 300));
                }
            } catch (e) {}
            return ret;
        };
    });

    console.log('[*] Hook installati. Apri Eventi nell\'app...');
});
