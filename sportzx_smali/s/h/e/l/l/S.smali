.class public final Ls/h/e/l/l/S;
.super Landroid/app/Application;
.source "SourceFile"


# static fields
.field public static isIsolated:Z

.field private static loadFromLib:Z

.field private static needX86Bridge:Z

.field private static perm:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/String;",
            "Ljava/util/Set",
            "<",
            "Ljava/lang/String;",
            ">;>;"
        }
    .end annotation
.end field

.field private static returnIntern:Z

.field public static strEntryApplication:Ljava/lang/String;

.field private static 伇:Ljava/lang/String;

.field private static 吹:Ljava/lang/String;

.field private static 岬:Landroid/app/Application;

.field private static 惂:Landroid/app/Application;

.field private static 祹:Landroid/content/Context;

.field private static 禂:Ljava/lang/String;

.field private static 緸:Ljava/lang/String;

.field private static 苟:Ljava/lang/String;

.field private static 鈦笔:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/Integer;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private static 钩:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .registers 3

    .prologue
    const/4 v2, 0x0

    const/4 v1, 0x0

    .line 43
    sput-object v1, Ls/h/e/l/l/S;->岬:Landroid/app/Application;

    .line 44
    const-string v0, "startApp"

    sput-object v0, Ls/h/e/l/l/S;->strEntryApplication:Ljava/lang/String;

    .line 45
    sput-object v1, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    .line 46
    const-string v0, "libijmDataEncryption"

    sput-object v0, Ls/h/e/l/l/S;->吹:Ljava/lang/String;

    .line 47
    const/4 v2, 0x0

    sput-boolean v2, Ls/h/e/l/l/S;->loadFromLib:Z

    .line 48
    const/4 v2, 0x0

    sput-boolean v2, Ls/h/e/l/l/S;->needX86Bridge:Z

    .line 50
    const/4 v0, 0x1

    const/4 v0, 0x1

    sput-boolean v0, Ls/h/e/l/l/S;->returnIntern:Z

    .line 51
    const/4 v2, 0x0

    sput-boolean v2, Ls/h/e/l/l/S;->isIsolated:Z

    .line 53
    sput-object v1, Ls/h/e/l/l/S;->禂:Ljava/lang/String;

    .line 54
    sput-object v1, Ls/h/e/l/l/S;->伇:Ljava/lang/String;

    .line 55
    sput-object v1, Ls/h/e/l/l/S;->钩:Ljava/lang/String;

    .line 56
    sput-object v1, Ls/h/e/l/l/S;->苟:Ljava/lang/String;

    .line 57
    sput-object v1, Ls/h/e/l/l/S;->緸:Ljava/lang/String;

    .line 58
    new-instance v0, Ljava/util/concurrent/ConcurrentHashMap;

    invoke-direct {v0}, Ljava/util/concurrent/ConcurrentHashMap;-><init>()V

    sput-object v0, Ls/h/e/l/l/S;->鈦笔:Ljava/util/Map;

    .line 59
    new-instance v0, Ljava/util/concurrent/ConcurrentHashMap;

    invoke-direct {v0}, Ljava/util/concurrent/ConcurrentHashMap;-><init>()V

    sput-object v0, Ls/h/e/l/l/S;->perm:Ljava/util/Map;

    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .prologue
    .line 42
    invoke-direct {p0}, Landroid/app/Application;-><init>()V

    return-void
.end method

.method public static native abcd65535(I)Ljava/lang/String;
.end method

.method public static native abcd65536(Landroid/app/Application;)V
.end method

.method public static native abcd65537(I)V
.end method

.method public static native abcd65538(Landroid/app/Application;)V
.end method

.method public static native abcd65570(Landroid/app/Application;Landroid/content/Context;)Z
.end method

.method public static native abcd65571(Landroid/app/Application;Landroid/content/Context;)Z
.end method

.method public static native abcd65572(Ldalvik/system/DexFile;)Ljava/util/Enumeration;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ldalvik/system/DexFile;",
            ")",
            "Ljava/util/Enumeration",
            "<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end method

.method public static native abcd65573(IJJJIIJ)J
.end method

.method public static native abcd65574()Z
.end method

.method public static native abcd65580(Landroid/content/res/AssetManager;Ljava/lang/String;)Landroid/content/res/AssetFileDescriptor;
.end method

.method public static native abcd65581(Ljava/lang/Class;Ljava/lang/String;)Ljava/io/InputStream;
.end method

.method public static native abcd65582(Ljava/lang/ClassLoader;Ljava/lang/String;)Ljava/io/InputStream;
.end method

.method public static native abcd65583(Ljava/util/zip/ZipFile;Ljava/lang/String;)Ljava/util/zip/ZipEntry;
.end method

.method public static native abcd65584(Landroid/content/res/AssetManager;Ljava/lang/String;)Ljava/io/InputStream;
.end method

.method public static abcdstr(I)Ljava/lang/String;
    .registers 4

    .prologue
    .line 240
    sget-object v0, Ls/h/e/l/l/S;->鈦笔:Ljava/util/Map;

    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-interface {v0, v1}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    .line 241
    if-nez v0, :cond_1b

    .line 242
    invoke-static {p0}, Ls/h/e/l/l/S;->abcd65535(I)Ljava/lang/String;

    move-result-object v0

    .line 243
    sget-object v1, Ls/h/e/l/l/S;->鈦笔:Ljava/util/Map;

    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    invoke-interface {v1, v2, v0}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 245
    :cond_1b
    if-eqz v0, :cond_25

    sget-boolean v1, Ls/h/e/l/l/S;->returnIntern:Z

    if-eqz v1, :cond_25

    .line 246
    invoke-virtual {v0}, Ljava/lang/String;->intern()Ljava/lang/String;

    move-result-object v0

    .line 248
    :cond_25
    return-object v0
.end method

.method public static abcdstr(Ljava/lang/String;)Ljava/lang/String;
    .registers 2

    .prologue
    .line 253
    :try_start_0
    invoke-static {p0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    .line 254
    invoke-static {v0}, Ls/h/e/l/l/S;->abcdstr(I)Ljava/lang/String;
    :try_end_7
    .catch Ljava/lang/NumberFormatException; {:try_start_0 .. :try_end_7} :catch_9

    move-result-object v0

    .line 258
    :goto_8
    return-object v0

    .line 255
    :catch_9
    move-exception v0

    .line 256
    invoke-virtual {v0}, Ljava/lang/NumberFormatException;->printStackTrace()V

    .line 258
    const/4 v0, 0x0

    goto :goto_8
.end method

.method public static getAppContext()Landroid/content/Context;
    .registers 1

    .prologue
    .line 75
    sget-object v0, Ls/h/e/l/l/S;->祹:Landroid/content/Context;

    return-object v0
.end method

.method public static getDir()Ljava/lang/String;
    .registers 1

    .prologue
    .line 71
    sget-object v0, Ls/h/e/l/l/S;->苟:Ljava/lang/String;

    return-object v0
.end method

.method public static getOrigApplicationContext(Landroid/content/Context;)Landroid/content/Context;
    .registers 2

    .prologue
    .line 79
    sget-object v0, Ls/h/e/l/l/S;->岬:Landroid/app/Application;

    if-ne p0, v0, :cond_6

    .line 80
    sget-object p0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    .line 82
    :cond_6
    return-object p0
.end method

.method public static getSoPath1()Ljava/lang/String;
    .registers 1

    .prologue
    .line 63
    sget-object v0, Ls/h/e/l/l/S;->伇:Ljava/lang/String;

    return-object v0
.end method

.method public static getSoPath2()Ljava/lang/String;
    .registers 1

    .prologue
    .line 67
    sget-object v0, Ls/h/e/l/l/S;->钩:Ljava/lang/String;

    return-object v0
.end method

.method public static native n0111()I
.end method

.method public static native n01121(J)Z
.end method

.method public static native n0112113(JII)Ljava/lang/Object;
.end method

.method public static native n011220(JJ)V
.end method

.method public static native n0112233(JJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01123(J)Ljava/lang/Object;
.end method

.method public static native n011230(JLjava/lang/Object;)V
.end method

.method public static native n011232(JLjava/lang/Object;)J
.end method

.method public static native n0113()Ljava/lang/Object;
.end method

.method public static native n01130(Ljava/lang/Object;)V
.end method

.method public static native n01131(Ljava/lang/Object;)Z
.end method

.method public static native n01133(Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113312(Ljava/lang/Object;Ljava/lang/Object;I)J
.end method

.method public static native n0113313(Ljava/lang/Object;Ljava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public static native n011333(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011333331333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method private 岬(Landroid/content/Context;)Ljava/lang/String;
    .registers 7

    .prologue
    const/4 v2, 0x1

    const/4 v1, 0x0

    .line 109
    sget-object v0, Landroid/os/Build;->CPU_ABI:Ljava/lang/String;

    const-string v3, "64"

    invoke-virtual {v0, v3}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-nez v0, :cond_16

    sget-object v0, Landroid/os/Build;->CPU_ABI2:Ljava/lang/String;

    const-string v3, "64"

    invoke-virtual {v0, v3}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-eqz v0, :cond_87

    :cond_16
    move v0, v2

    .line 110
    :goto_17
    invoke-virtual {p1}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v3

    invoke-virtual {v3}, Ljava/io/File;->getParentFile()Ljava/io/File;

    move-result-object v3

    invoke-virtual {v3}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v3

    .line 112
    :try_start_23
    invoke-virtual {p1}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v4

    invoke-virtual {v4}, Ljava/io/File;->getParentFile()Ljava/io/File;

    move-result-object v4

    invoke-virtual {v4}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;
    :try_end_2e
    .catch Ljava/lang/Exception; {:try_start_23 .. :try_end_2e} :catch_8e

    move-result-object v3

    .line 116
    :goto_2f
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v4, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "/.abcedf"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    .line 117
    invoke-static {v3, v1}, Ls/h/e/l/l/S;->岬(Ljava/lang/String;Z)Ljava/lang/String;

    move-result-object v1

    sput-object v1, Ls/h/e/l/l/S;->禂:Ljava/lang/String;

    .line 118
    if-nez v0, :cond_89

    sget-object v0, Ls/h/e/l/l/S;->禂:Ljava/lang/String;

    :goto_4c
    sput-object v0, Ls/h/e/l/l/S;->緸:Ljava/lang/String;

    .line 119
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ls/h/e/l/l/S;->禂:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sput-object v0, Ls/h/e/l/l/S;->伇:Ljava/lang/String;

    .line 120
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ls/h/e/l/l/S;->緸:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sput-object v0, Ls/h/e/l/l/S;->钩:Ljava/lang/String;

    .line 121
    sput-object v3, Ls/h/e/l/l/S;->苟:Ljava/lang/String;

    .line 122
    return-object v3

    :cond_87
    move v0, v1

    .line 109
    goto :goto_17

    .line 118
    :cond_89
    invoke-static {v3, v2}, Ls/h/e/l/l/S;->岬(Ljava/lang/String;Z)Ljava/lang/String;

    move-result-object v0

    goto :goto_4c

    :catch_8e
    move-exception v4

    goto :goto_2f
.end method

.method private static 岬(Ljava/lang/String;Z)Ljava/lang/String;
    .registers 5

    .prologue
    .line 196
    sget-object v0, Ls/h/e/l/l/S;->吹:Ljava/lang/String;

    .line 197
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x17

    if-ge v1, v2, :cond_1d

    .line 198
    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    move-result v1

    .line 199
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 201
    :cond_1d
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    if-eqz p1, :cond_33

    const-string v0, "_64.so"

    :goto_2a
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_33
    const-string v0, ".so"

    goto :goto_2a
.end method


# virtual methods
.method protected final attachBaseContext(Landroid/content/Context;)V
    .registers 10

    .prologue
    const/4 v2, 0x0

    const/4 v3, 0x1

    .line 127
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 128
    invoke-super {p0, p1}, Landroid/app/Application;->attachBaseContext(Landroid/content/Context;)V

    .line 129
    invoke-static {}, Lv/m/岬;->惂()V

    .line 130
    sput-object p1, Ls/h/e/l/l/S;->祹:Landroid/content/Context;

    .line 132
    const-string v0, "RMUTGF_KEY"

    const-string v1, "s\u007f}>c`\u007fbdjh>|yfu"

    invoke-static {v0, v1}, Ljava/lang/System;->setProperty(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    .line 133
    sget-object v0, Ls/h/e/l/l/S;->岬:Landroid/app/Application;

    if-nez v0, :cond_1a

    .line 134
    sput-object p0, Ls/h/e/l/l/S;->岬:Landroid/app/Application;

    .line 136
    :cond_1a
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    if-nez v0, :cond_51

    .line 137
    invoke-static {}, Lv/m/岬;->岬()Z

    move-result v4

    .line 138
    sget-object v0, Landroid/os/Build;->CPU_ABI:Ljava/lang/String;

    const-string v1, "64"

    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-nez v0, :cond_36

    sget-object v0, Landroid/os/Build;->CPU_ABI2:Ljava/lang/String;

    const-string v1, "64"

    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-eqz v0, :cond_a2

    :cond_36
    move v1, v3

    .line 139
    :goto_37
    if-eqz v4, :cond_42

    sget-boolean v0, Ls/h/e/l/l/S;->needX86Bridge:Z

    if-eqz v0, :cond_42

    .line 140
    const-string v0, "X86Bridge"

    invoke-static {v0, v3}, Lv/m/岬;->岬(Ljava/lang/String;Z)V

    .line 141
    :cond_42
    sget-boolean v0, Ls/h/e/l/l/S;->loadFromLib:Z

    if-eqz v0, :cond_aa

    .line 142
    if-eqz v4, :cond_a4

    sget-boolean v0, Ls/h/e/l/l/S;->needX86Bridge:Z

    if-nez v0, :cond_a4

    .line 143
    const-string v0, "ijmDataEncryption_x86"

    invoke-static {v0, v3}, Lv/m/岬;->岬(Ljava/lang/String;Z)V

    .line 162
    :cond_51
    :goto_51
    invoke-static {}, Lv/m/q;->begin()V

    .line 163
    sget-boolean v0, Ls/h/e/l/l/S;->isIsolated:Z

    if-nez v0, :cond_a1

    .line 164
    sget-object v0, Ls/h/e/l/l/S;->岬:Landroid/app/Application;

    invoke-static {v0}, Ls/h/e/l/l/S;->abcd65536(Landroid/app/Application;)V

    .line 165
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    if-nez v0, :cond_a1

    .line 167
    :try_start_61
    invoke-virtual {p1}, Landroid/content/Context;->getClassLoader()Ljava/lang/ClassLoader;

    move-result-object v0

    .line 168
    if-eqz v0, :cond_77

    .line 169
    sget-object v1, Ls/h/e/l/l/S;->strEntryApplication:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/ClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 170
    if-eqz v0, :cond_77

    .line 171
    invoke-virtual {v0}, Ljava/lang/Class;->newInstance()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/app/Application;

    sput-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;
    :try_end_77
    .catch Ljava/lang/Exception; {:try_start_61 .. :try_end_77} :catch_161

    .line 175
    :cond_77
    :goto_77
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    if-eqz v0, :cond_15c

    .line 178
    :try_start_7b
    const-class v0, Landroid/app/Application;

    const-string v1, "attach"

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Class;

    const/4 v3, 0x0

    const-class v4, Landroid/content/Context;

    aput-object v4, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    .line 180
    if-eqz v0, :cond_9c

    .line 181
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 182
    sget-object v1, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p1, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_9c
    .catch Ljava/lang/Exception; {:try_start_7b .. :try_end_9c} :catch_153

    .line 187
    :cond_9c
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    invoke-static {v0, p1}, Ls/h/e/l/l/S;->abcd65571(Landroid/app/Application;Landroid/content/Context;)Z

    .line 193
    :cond_a1
    :goto_a1
    return-void

    :cond_a2
    move v1, v2

    .line 138
    goto :goto_37

    .line 145
    :cond_a4
    const-string v0, "ijmDataEncryption"

    invoke-static {v0, v3}, Lv/m/岬;->岬(Ljava/lang/String;Z)V

    goto :goto_51

    .line 148
    :cond_aa
    invoke-direct {p0, p1}, Ls/h/e/l/l/S;->岬(Landroid/content/Context;)Ljava/lang/String;

    move-result-object v5

    .line 149
    if-eqz v4, :cond_111

    sget-boolean v0, Ls/h/e/l/l/S;->needX86Bridge:Z

    if-nez v0, :cond_111

    const-string v0, "_x86.so"

    .line 150
    :goto_b6
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v7, Ls/h/e/l/l/S;->吹:Ljava/lang/String;

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v6, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sget-object v6, Ls/h/e/l/l/S;->禂:Ljava/lang/String;

    invoke-static {p1, v0, v5, v6}, Lv/m/岬;->岬(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z

    .line 151
    if-eqz v1, :cond_135

    .line 152
    if-eqz v4, :cond_114

    sget-boolean v0, Ls/h/e/l/l/S;->needX86Bridge:Z

    if-nez v0, :cond_114

    const-string v0, "_x64.so"

    .line 153
    :goto_d8
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v4, Ls/h/e/l/l/S;->吹:Ljava/lang/String;

    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sget-object v1, Ls/h/e/l/l/S;->緸:Ljava/lang/String;

    invoke-static {p1, v0, v5, v1}, Lv/m/岬;->岬(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_117

    .line 154
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ls/h/e/l/l/S;->緸:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0, v2}, Lv/m/岬;->岬(Ljava/lang/String;Z)V

    goto/16 :goto_51

    .line 149
    :cond_111
    const-string v0, ".so"

    goto :goto_b6

    .line 152
    :cond_114
    const-string v0, "_a64.so"

    goto :goto_d8

    .line 156
    :cond_117
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ls/h/e/l/l/S;->禂:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0, v2}, Lv/m/岬;->岬(Ljava/lang/String;Z)V

    goto/16 :goto_51

    .line 158
    :cond_135
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Ls/h/e/l/l/S;->禂:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0, v2}, Lv/m/岬;->岬(Ljava/lang/String;Z)V

    goto/16 :goto_51

    .line 184
    :catch_153
    move-exception v0

    .line 185
    new-instance v1, Ljava/lang/RuntimeException;

    const-string v2, "Failed to call attachBaseContext."

    invoke-direct {v1, v2, v0}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;Ljava/lang/Throwable;)V

    throw v1

    .line 189
    :cond_15c
    invoke-static {v3}, Ljava/lang/System;->exit(I)V

    goto/16 :goto_a1

    :catch_161
    move-exception v0

    goto/16 :goto_77
.end method

.method public native n1110()V
.end method

.method public native n11111112(IIZI)J
.end method

.method public native n11120(J)V
.end method

.method public native n11121(J)Z
.end method

.method public native n11123(J)Ljava/lang/Object;
.end method

.method public native n111230(JLjava/lang/Object;)V
.end method

.method public native n111231(JLjava/lang/Object;)I
.end method

.method public native n1112311(JLjava/lang/Object;I)I
.end method

.method public native n1112311111211(JLjava/lang/Object;IIIZIJI)I
.end method

.method public native n1112313311(JLjava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;I)I
.end method

.method public native n111232(JLjava/lang/Object;)J
.end method

.method public native n1112331(JLjava/lang/Object;Ljava/lang/Object;)I
.end method

.method public native n1113()Ljava/lang/Object;
.end method

.method public native n11130(Ljava/lang/Object;)V
.end method

.method public native n1113112(Ljava/lang/Object;IF)J
.end method

.method public native n111313111(Ljava/lang/Object;ILjava/lang/Object;FF)I
.end method

.method public native n111331112(Ljava/lang/Object;Ljava/lang/Object;ZII)J
.end method

.method public native n111333(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11133331333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public final onCreate()V
    .registers 6

    .prologue
    .line 88
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 89
    invoke-super {p0}, Landroid/app/Application;->onCreate()V

    .line 93
    sget-object v0, Ls/h/e/l/l/S;->岬:Landroid/app/Application;

    invoke-virtual {v0}, Landroid/app/Application;->getBaseContext()Landroid/content/Context;

    move-result-object v0

    .line 95
    :try_start_c
    sget-object v1, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    invoke-static {v1, v0}, Ls/h/e/l/l/S;->abcd65570(Landroid/app/Application;Landroid/content/Context;)Z
    :try_end_11
    .catch Ljava/lang/Exception; {:try_start_c .. :try_end_11} :catch_63

    .line 99
    :goto_11
    sget-boolean v0, Ls/h/e/l/l/S;->isIsolated:Z

    if-nez v0, :cond_35

    .line 100
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    if-eqz v0, :cond_1e

    .line 101
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    invoke-virtual {v0}, Landroid/app/Application;->onCreate()V

    .line 103
    :cond_1e
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    invoke-static {v0}, Ls/h/e/l/l/S;->abcd65538(Landroid/app/Application;)V

    .line 104
    sget-object v0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    if-eqz v0, :cond_29

    sget-object p0, Ls/h/e/l/l/S;->惂:Landroid/app/Application;

    :cond_29
    sget-object v0, Ls/h/e/l/l/S;->祹:Landroid/content/Context;

    .line 1275
    if-eqz p0, :cond_35

    if-eqz v0, :cond_35

    invoke-static {v0}, Lv/m/岬;->岬(Landroid/content/Context;)Z

    move-result v0

    if-nez v0, :cond_36

    .line 1284
    :cond_35
    :goto_35
    return-void

    .line 1278
    :cond_36
    :try_start_36
    const-string v0, "s\u007f}>zw>rx>Bu`\u007fbdcDy}u"

    invoke-static {v0}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 1279
    const-string v1, "BuwycdubQsdyfydiSq||Rqs{c"

    invoke-static {v1}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Class;

    const/4 v3, 0x0

    const-class v4, Landroid/app/Application;

    aput-object v4, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    .line 1280
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 1281
    const/4 v1, 0x0

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p0, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_60
    .catch Ljava/lang/Exception; {:try_start_36 .. :try_end_60} :catch_61

    goto :goto_35

    :catch_61
    move-exception v0

    goto :goto_35

    :catch_63
    move-exception v0

    goto :goto_11
.end method
