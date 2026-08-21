.class public final Lv/m/岬;
.super Ljava/lang/Object;


# direct methods
.method public static 岬(Ljava/lang/String;)Ljava/lang/String;
    .registers 12

    const/4 v2, 0x0

    const/4 v4, 0x0

    const-string v0, "\u06db\u06eb\u06e7\u06e0\u06e2\u06df\u06e0\u06ec\u06d6\u06e7\u06d7\u06e7\u06e8\u06e5\u06dc\u06dc\u06d8\u06e5\u06d8\u06e0\u06e7\u06db\u06eb\u06e2\u06e5\u06e1\u06eb\u06d8\u06d8"

    move-object v1, v2

    move v3, v4

    move v5, v4

    move-object v6, v2

    move-object v7, v2

    move-object v8, v2

    :goto_a
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v2

    const/16 v9, 0x12b

    const v10, 0x623e60e1

    xor-int/2addr v2, v9

    xor-int/2addr v2, v10

    sparse-switch v2, :sswitch_data_a4

    goto :goto_a

    :sswitch_19
    const-string v0, "\u06d6\u06e0\u06e8\u06d8\u06e2\u06dc\u06d8\u06eb\u06d8\u06d7\u06e4\u06e5\u06d8\u06db\u06e6\u06e5\u06d8\u06e6\u06d8\u06ec\u06ec\u06ec\u06ec\u06d7\u06e4\u06d6"

    goto :goto_a

    :sswitch_1c
    const v2, -0x6fda5ad8

    const-string v0, "\u06d7\u06e2\u06da\u06e5\u06df\u06e6\u06df\u06db\u06da\u06ec\u06db\u06e1\u06df\u06e8\u06d8\u06d8\u06d7\u06d7\u06e0\u06e7\u06e0\u06eb\u06dc\u06e8\u06d6\u06db\u06da\u06e0"

    :goto_21
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v9

    xor-int/2addr v9, v2

    sparse-switch v9, :sswitch_data_e6

    goto :goto_21

    :sswitch_2a
    const-string v0, "\u06d9\u06ec\u06e6\u06e6\u06e2\u06d9\u06d6\u06e1\u06dc\u06e6\u06e1\u06eb\u06e1\u06ec\u06d8\u06d8\u06e8\u06e2\u06e5\u06d8\u06df\u06d7\u06d7\u06d6\u06d7\u06d9\u06e1\u06d6"

    goto :goto_a

    :cond_2d
    const-string v0, "\u06d6\u06d6\u06df\u06dc\u06e7\u06e5\u06d8\u06df\u06db\u06d8\u06e0\u06df\u06e6\u06d8\u06e8\u06e1\u06d8\u06d6\u06e7\u06e2"

    goto :goto_21

    :sswitch_30
    invoke-static {p0}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    move-result v0

    if-eqz v0, :cond_2d

    const-string v0, "\u06e7\u06df\u06ec\u06d6\u06d6\u06e5\u06dc\u06e2\u06df\u06da\u06e1\u06e1\u06da\u06e5\u06dc\u06d8\u06e6\u06d8\u06e5\u06d8\u06e1\u06d6\u06d8\u06e0\u06e2\u06eb"

    goto :goto_21

    :sswitch_39
    const-string v0, "\u06dc\u06d9\u06e0\u06e0\u06db\u06e6\u06d8\u06dc\u06df\u06d6\u06d6\u06d6\u06d8\u06da\u06da\u06ec\u06d8\u06db\u06da\u06ec\u06d9\u06e7"

    goto :goto_21

    :sswitch_3c
    const-string v8, ""

    const-string v0, "\u06e2\u06d6\u06e8\u06e4\u06da\u06df\u06df\u06d8\u06e8\u06d8\u06ec\u06dc\u06e1\u06e5\u06d7\u06e4\u06e2\u06db\u06d6\u06d8\u06db\u06e8\u06e2\u06dc\u06e7\u06e1\u06d8\u06e6\u06da\u06da"

    goto :goto_a

    :sswitch_41
    const-string v0, "\u06d9\u06e6\u06d6\u06d6\u06e1\u06e7\u06d8\u06e1\u06dc\u06e1\u06d8\u06e0\u06e0\u06da\u06e4\u06e1\u06ec\u06df\u06eb\u06e0"

    move-object v7, v8

    goto :goto_a

    :sswitch_45
    invoke-virtual {p0}, Ljava/lang/String;->toCharArray()[C

    move-result-object v2

    const-string v0, "\u06ec\u06d9\u06da\u06ec\u06e4\u06dc\u06da\u06eb\u06d6\u06e8\u06df\u06e8\u06dc\u06d6\u06e8\u06e0\u06d6\u06ec\u06e8\u06e4\u06e7\u06e8\u06e7\u06da\u06e1\u06e8\u06e8"

    move-object v6, v2

    goto :goto_a

    :sswitch_4d
    const-string v0, "\u06d8\u06e2\u06e0\u06d8\u06d7\u06d9\u06da\u06e1\u06e5\u06d8\u06db\u06d6\u06d7\u06e8\u06d9\u06da"

    goto :goto_a

    :sswitch_50
    const-string v0, "\u06dc\u06dc\u06df\u06db\u06d9\u06d7\u06dc\u06eb\u06e8\u06d8\u06e0\u06d8\u06d7\u06d8\u06dc\u06d8"

    move v5, v4

    goto :goto_a

    :sswitch_54
    const v2, 0x17e2fcd5

    const-string v0, "\u06d7\u06da\u06df\u06db\u06e5\u06e7\u06e0\u06dc\u06e0\u06e2\u06e6\u06db\u06db\u06e7"

    :goto_59
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v9

    xor-int/2addr v9, v2

    sparse-switch v9, :sswitch_data_f8

    goto :goto_59

    :sswitch_62
    const-string v0, "\u06d9\u06e6\u06e7\u06d8\u06e4\u06e8\u06dc\u06d8\u06ec\u06d7\u06e8\u06da\u06ec\u06e8\u06e4\u06e8\u06d9\u06e4\u06e7\u06d8\u06dc\u06e2\u06d8\u06e6\u06d8\u06d8\u06eb\u06da\u06d6\u06d8"

    goto :goto_59

    :cond_65
    const-string v0, "\u06d9\u06eb\u06e2\u06e4\u06da\u06e5\u06d8\u06d6\u06e7\u06e1\u06d8\u06e2\u06e6\u06db\u06e6\u06ec\u06e5\u06e4\u06eb\u06da\u06e7\u06eb\u06d6\u06d8\u06db\u06ec\u06eb\u06ec\u06e4\u06d8"

    goto :goto_59

    :sswitch_68
    array-length v0, v6

    if-ge v5, v0, :cond_65

    const-string v0, "\u06da\u06e4\u06eb\u06eb\u06e7\u06e7\u06d7\u06e8\u06e7\u06d9\u06e6\u06d8\u06d8\u06e0\u06dc\u06d8\u06e5\u06e2\u06d6\u06d8"

    goto :goto_59

    :sswitch_6e
    const-string v0, "\u06e0\u06e5\u06ec\u06df\u06d6\u06ec\u06d7\u06da\u06e8\u06d8\u06d8\u06e0\u06eb\u06da\u06e5\u06e5\u06db\u06e5\u06d7"

    goto :goto_a

    :sswitch_71
    aget-char v0, v6, v5

    xor-int/lit8 v0, v0, 0x10

    int-to-char v0, v0

    aput-char v0, v6, v5

    const-string v0, "\u06e8\u06e2\u06e5\u06d8\u06e2\u06eb\u06e1\u06e8\u06d8\u06d6\u06d8\u06e5\u06ec\u06e5\u06db\u06df\u06d6\u06e1\u06d6\u06d9\u06e4\u06ec\u06da"

    goto :goto_a

    :sswitch_7b
    add-int/lit8 v2, v5, 0x1

    const-string v0, "\u06db\u06e0\u06db\u06d8\u06d7\u06e6\u06d8\u06e8\u06df\u06e6\u06d8\u06d7\u06e4\u06dc\u06db\u06e2\u06e6\u06e5\u06da\u06d8\u06d8"

    move v3, v2

    goto :goto_a

    :sswitch_81
    const-string v0, "\u06ec\u06d7\u06d8\u06dc\u06d9\u06d8\u06e1\u06db\u06df\u06da\u06d9\u06e5\u06d8\u06d9\u06e1\u06eb\u06ec\u06e2\u06dc\u06d8\u06e8\u06ec\u06e7\u06e7\u06e4\u06e5\u06d8\u06d7\u06e5\u06d9"

    move v5, v3

    goto :goto_a

    :sswitch_85
    invoke-static {v6}, Ljava/lang/String;->valueOf([C)Ljava/lang/String;

    move-result-object v1

    const-string v0, "\u06eb\u06da\u06ec\u06df\u06e7\u06e1\u06d7\u06db\u06e4\u06e0\u06e4\u06e2\u06e6\u06e4\u06dc"

    goto/16 :goto_a

    :sswitch_8d
    const-string v0, "\u06e4\u06e1\u06dc\u06dc\u06da\u06d6\u06d8\u06d7\u06e8\u06e1\u06e0\u06ec\u06da\u06e7\u06e1\u06df\u06d8\u06eb\u06e7"

    move-object v7, v1

    goto/16 :goto_a

    :sswitch_92
    const-string v0, "\u06d9\u06e6\u06d6\u06d6\u06e1\u06e7\u06d8\u06e1\u06dc\u06e1\u06d8\u06e0\u06e0\u06da\u06e4\u06e1\u06ec\u06df\u06eb\u06e0"

    goto/16 :goto_a

    :sswitch_96
    const-string v0, "\u06d6\u06e0\u06db\u06e1\u06d8\u06e8\u06e2\u06e0\u06e1\u06d8\u06df\u06eb\u06d6\u06d8\u06d8\u06ec\u06e1\u06e5\u06d8\u06e6\u06d9\u06e7\u06d7\u06d9\u06e4"

    goto/16 :goto_a

    :sswitch_9a
    const-string v0, "\u06dc\u06dc\u06df\u06db\u06d9\u06d7\u06dc\u06eb\u06e8\u06d8\u06e0\u06d8\u06d7\u06d8\u06dc\u06d8"

    goto/16 :goto_a

    :sswitch_9e
    const-string v0, "\u06e2\u06da\u06dc\u06e6\u06db\u06eb\u06e2\u06d6\u06e1\u06d7\u06e7\u06d6\u06e8\u06e1\u06d6\u06e0\u06e2\u06d7"

    goto/16 :goto_a

    :sswitch_a2
    return-object v7

    nop

    :sswitch_data_a4
    .sparse-switch
        -0x6e19e24b -> :sswitch_19
        -0x6410381f -> :sswitch_45
        -0x3791da8b -> :sswitch_7b
        -0x2aa93cbc -> :sswitch_54
        -0x14b8121f -> :sswitch_50
        0x1b3bc1ff -> :sswitch_81
        0x2b60c9df -> :sswitch_71
        0x35b3dc49 -> :sswitch_85
        0x35b59c85 -> :sswitch_3c
        0x3cfa4162 -> :sswitch_a2
        0x40df474e -> :sswitch_9a
        0x5c147286 -> :sswitch_92
        0x5e023a82 -> :sswitch_1c
        0x6797bbae -> :sswitch_8d
        0x6d6fe2c3 -> :sswitch_41
        0x6e5e1c4c -> :sswitch_4d
    .end sparse-switch

    :sswitch_data_e6
    .sparse-switch
        -0x62600c0e -> :sswitch_2a
        -0x4648bf76 -> :sswitch_96
        0x18be166c -> :sswitch_39
        0x194a864b -> :sswitch_30
    .end sparse-switch

    :sswitch_data_f8
    .sparse-switch
        -0x45b60b09 -> :sswitch_62
        0x16dc05a3 -> :sswitch_9e
        0x3b103be9 -> :sswitch_6e
        0x635d3615 -> :sswitch_68
    .end sparse-switch
.end method

.method private static 岬(Ljava/io/Closeable;)V
    .registers 4

    const v1, 0x3914388b

    const-string v0, "\u06e8\u06e7\u06db\u06d7\u06d7\u06d8\u06d8\u06e2\u06e7\u06e7\u06d8\u06e4\u06e5\u06d8\u06e6\u06e8\u06d8\u06dc\u06e6\u06e5\u06d7\u06dc\u06e6"

    :goto_5
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v2

    xor-int/2addr v2, v1

    sparse-switch v2, :sswitch_data_20

    goto :goto_5

    :sswitch_e
    if-eqz p0, :cond_13

    const-string v0, "\u06da\u06da\u06e8\u06d8\u06d7\u06e5\u06dc\u06e5\u06d7\u06e2\u06e2\u06e6\u06e7\u06db\u06e6\u06e0"

    goto :goto_5

    :cond_13
    const-string v0, "\u06df\u06db\u06e5\u06d8\u06d9\u06e6\u06e2\u06df\u06db\u06d7\u06e4\u06e5\u06ec\u06eb\u06da\u06e1\u06d8"

    goto :goto_5

    :sswitch_16
    const-string v0, "\u06d9\u06df\u06dc\u06d8\u06e0\u06e1\u06dc\u06e4\u06e2\u06e8\u06d8\u06e1\u06e4\u06e5\u06da\u06e7\u06d8\u06ec\u06da\u06e1\u06d9\u06d8\u06e5\u06e6\u06da"

    goto :goto_5

    :sswitch_19
    :try_start_19
    invoke-interface {p0}, Ljava/io/Closeable;->close()V
    :try_end_1c
    .catch Ljava/io/IOException; {:try_start_19 .. :try_end_1c} :catch_1d

    :goto_1c
    :sswitch_1c
    return-void

    :catch_1d
    move-exception v0

    goto :goto_1c

    nop

    :sswitch_data_20
    .sparse-switch
        -0x445de4a4 -> :sswitch_e
        0x981a12f -> :sswitch_16
        0xd87f557 -> :sswitch_1c
        0x583cd59c -> :sswitch_19
    .end sparse-switch
.end method

.method private static 岬(Ljava/io/File;)V
    .registers 7

    const/4 v5, 0x0

    const/4 v4, 0x1

    const-string v0, "\u06d8\u06e5\u06d6\u06d8\u06ec\u06e0\u06e5\u06d8\u06e2\u06df\u06e1\u06d9\u06e5\u06dc\u06e7\u06df\u06e6\u06d8\u06eb\u06db\u06dc\u06eb\u06db\u06db\u06db\u06ec\u06d8\u06d8\u06e7\u06dc\u06d7"

    :goto_4
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v1

    const/16 v2, 0x36a

    const v3, -0x4901e570

    xor-int/2addr v1, v2

    xor-int/2addr v1, v3

    sparse-switch v1, :sswitch_data_50

    goto :goto_4

    :sswitch_13
    const-string v0, "\u06e0\u06dc\u06e8\u06eb\u06da\u06da\u06d8\u06d6\u06ec\u06dc\u06d8\u06d8\u06dc\u06ec\u06d6\u06e4\u06e8\u06dc\u06d8\u06e7\u06e2\u06eb"

    goto :goto_4

    :sswitch_16
    const v1, 0x1a901716

    const-string v0, "\u06d7\u06e5\u06db\u06e2\u06e8\u06df\u06eb\u06e8\u06e6\u06e6\u06e4\u06ec\u06e0\u06e8\u06e7\u06db\u06d7\u06dc\u06ec\u06ec\u06dc\u06e1\u06e0\u06d6\u06d8"

    :goto_1b
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v2

    xor-int/2addr v2, v1

    sparse-switch v2, :sswitch_data_6e

    goto :goto_1b

    :sswitch_24
    const-string v0, "\u06d8\u06d7\u06d9\u06e7\u06d9\u06d7\u06d8\u06d8\u06d8\u06d8\u06d9\u06e6\u06dc\u06e4\u06d9\u06e8\u06e5\u06e2\u06e0\u06dc\u06dc\u06d8\u06e8\u06e4\u06d6"

    goto :goto_1b

    :cond_27
    const-string v0, "\u06ec\u06ec\u06e0\u06db\u06d7\u06dc\u06d8\u06e8\u06e6\u06e6\u06d8\u06e6\u06d9\u06e6\u06d8\u06e6\u06e8\u06d9\u06eb\u06df\u06e2"

    goto :goto_1b

    :sswitch_2a
    invoke-virtual {p0}, Ljava/io/File;->exists()Z

    move-result v0

    if-nez v0, :cond_27

    const-string v0, "\u06df\u06d9\u06eb\u06eb\u06dc\u06eb\u06e5\u06db\u06eb\u06d8\u06db\u06dc\u06e8\u06e1\u06d8\u06eb\u06eb\u06d7\u06e8\u06d8\u06d8\u06d8\u06dc\u06d8\u06d8\u06e8\u06eb\u06eb"

    goto :goto_1b

    :sswitch_33
    const-string v0, "\u06e4\u06e2\u06e5\u06d8\u06d6\u06da\u06e1\u06d8\u06e1\u06e5\u06d9\u06e5\u06e0\u06e8\u06d7\u06d8\u06d6\u06eb\u06eb\u06d6\u06d8\u06e1\u06df\u06e4\u06e8\u06ec\u06e1\u06d8\u06eb\u06e4\u06e6\u06d8"

    goto :goto_4

    :sswitch_36
    invoke-virtual {p0, v4, v4}, Ljava/io/File;->setReadable(ZZ)Z

    const-string v0, "\u06e6\u06df\u06d8\u06dc\u06e8\u06e1\u06d8\u06d9\u06d6\u06df\u06d9\u06dc\u06d9\u06e6\u06e1\u06ec\u06df\u06d7\u06e5\u06d8\u06d6\u06d8\u06dc\u06d7\u06e5\u06df\u06dc\u06dc"

    goto :goto_4

    :sswitch_3c
    invoke-virtual {p0, v4, v4}, Ljava/io/File;->setExecutable(ZZ)Z

    const-string v0, "\u06d6\u06d7\u06d8\u06d8\u06ec\u06e1\u06e1\u06d8\u06d8\u06d6\u06e6\u06dc\u06d7\u06df\u06df\u06e5\u06db\u06db\u06e6\u06e2\u06db\u06df"

    goto :goto_4

    :sswitch_42
    invoke-virtual {p0, v5, v5}, Ljava/io/File;->setWritable(ZZ)Z

    const-string v0, "\u06d7\u06da\u06db\u06d9\u06ec\u06df\u06d8\u06e8\u06eb\u06e4\u06df\u06da\u06e5\u06e8\u06e7\u06df\u06ec\u06eb\u06e1\u06dc\u06e2\u06eb\u06db\u06dc\u06db\u06ec"

    goto :goto_4

    :sswitch_48
    const-string v0, "\u06e4\u06e2\u06e5\u06d8\u06d6\u06da\u06e1\u06d8\u06e1\u06e5\u06d9\u06e5\u06e0\u06e8\u06d7\u06d8\u06d6\u06eb\u06eb\u06d6\u06d8\u06e1\u06df\u06e4\u06e8\u06ec\u06e1\u06d8\u06eb\u06e4\u06e6\u06d8"

    goto :goto_4

    :sswitch_4b
    const-string v0, "\u06da\u06e1\u06e4\u06d8\u06e6\u06e4\u06eb\u06d6\u06ec\u06db\u06e2\u06dc\u06d8\u06d7\u06e1\u06ec\u06eb\u06d9\u06e8\u06d8\u06e2\u06e8\u06db\u06ec\u06d8\u06e7\u06e0\u06e0\u06e6\u06d8"

    goto :goto_4

    :sswitch_4e
    return-void

    nop

    :sswitch_data_50
    .sparse-switch
        -0x5d6de6d3 -> :sswitch_16
        -0x33c7128b -> :sswitch_42
        -0x270c0809 -> :sswitch_36
        -0x24f6f16e -> :sswitch_48
        0x4fa2ec7 -> :sswitch_3c
        0x14e4919c -> :sswitch_13
        0x6fefb1e3 -> :sswitch_4e
    .end sparse-switch

    :sswitch_data_6e
    .sparse-switch
        -0x7e7fbc4e -> :sswitch_4b
        -0x6d99ca63 -> :sswitch_2a
        0x29762d17 -> :sswitch_24
        0x587c3080 -> :sswitch_33
    .end sparse-switch
.end method

.method public static 岬(Ljava/lang/String;Z)V
    .registers 6

    const-string v0, "\u06ec\u06d7\u06e5\u06df\u06e5\u06d6\u06d8\u06e4\u06eb\u06d8\u06d8\u06e6\u06eb\u06db\u06df\u06da\u06e5\u06d8"

    :goto_2
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v1

    const/16 v2, 0x107

    const v3, -0x3ea20614

    xor-int/2addr v1, v2

    xor-int/2addr v1, v3

    sparse-switch v1, :sswitch_data_46

    goto :goto_2

    :sswitch_11
    const-string v0, "\u06e8\u06e0\u06e1\u06d6\u06eb\u06ec\u06e1\u06e2\u06df\u06e5\u06ec\u06eb\u06e8\u06d7\u06d8\u06d8\u06eb\u06e8\u06dc\u06d8"

    goto :goto_2

    :sswitch_14
    const-string v0, "\u06e2\u06e2\u06e0\u06e5\u06e4\u06e1\u06d8\u06e0\u06e1\u06e0\u06e5\u06db\u06e1\u06dc\u06ec\u06e0"

    goto :goto_2

    :sswitch_17
    const v1, -0x44f06e71

    const-string v0, "\u06e4\u06eb\u06e6\u06d8\u06db\u06e2\u06e6\u06df\u06d7\u06df\u06da\u06e7\u06e8\u06d8\u06dc\u06ec\u06db\u06e0\u06e6\u06e1\u06e8\u06d8\u06e8\u06db\u06d8\u06e1"

    :goto_1c
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v2

    xor-int/2addr v2, v1

    sparse-switch v2, :sswitch_data_64

    goto :goto_1c

    :sswitch_25
    const-string v0, "\u06da\u06df\u06e8\u06da\u06d9\u06e5\u06d8\u06db\u06ec\u06eb\u06e2\u06ec\u06dc\u06e2\u06e4\u06e8\u06e4\u06eb"

    goto :goto_2

    :cond_28
    const-string v0, "\u06d7\u06d9\u06ec\u06e4\u06d6\u06e5\u06d8\u06d9\u06e0\u06e6\u06e6\u06dc\u06e1\u06e0\u06d6\u06d8"

    goto :goto_1c

    :sswitch_2b
    if-eqz p1, :cond_28

    const-string v0, "\u06e5\u06d6\u06db\u06d7\u06db\u06e5\u06e6\u06e7\u06dc\u06e5\u06d9\u06d8\u06d8\u06da\u06e1\u06d8\u06d8\u06e0\u06eb\u06d6"

    goto :goto_1c

    :sswitch_30
    const-string v0, "\u06d8\u06e8\u06e7\u06e7\u06dc\u06d8\u06e0\u06d7\u06e6\u06d8\u06e4\u06e8\u06db\u06e1\u06da\u06eb\u06e6\u06da\u06df\u06e5\u06e4\u06e1\u06d8"

    goto :goto_1c

    :sswitch_33
    const-string v0, "\u06db\u06e8\u06e2\u06df\u06d6\u06e2\u06dc\u06da\u06da\u06d7\u06eb\u06e7\u06e0\u06e1\u06ec"

    goto :goto_2

    :sswitch_36
    invoke-static {p0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    const-string v0, "\u06db\u06d8\u06dc\u06d7\u06e7\u06df\u06db\u06e4\u06da\u06da\u06d6\u06d8\u06df\u06d7\u06ec\u06e7\u06da\u06e6\u06e2\u06da\u06e6\u06d6\u06db\u06e5\u06e0\u06d8"

    goto :goto_2

    :sswitch_3c
    invoke-static {p0}, Ljava/lang/System;->load(Ljava/lang/String;)V

    const-string v0, "\u06eb\u06e2\u06eb\u06e1\u06e0\u06e4\u06df\u06e4\u06e6\u06df\u06d7\u06e6\u06d6\u06d8\u06d8\u06e0\u06d9\u06e8\u06d8\u06e2\u06da\u06e4\u06e6\u06e4\u06e0"

    goto :goto_2

    :sswitch_42
    const-string v0, "\u06db\u06d8\u06dc\u06d7\u06e7\u06df\u06db\u06e4\u06da\u06da\u06d6\u06d8\u06df\u06d7\u06ec\u06e7\u06da\u06e6\u06e2\u06da\u06e6\u06d6\u06db\u06e5\u06e0\u06d8"

    goto :goto_2

    :sswitch_45
    return-void

    :sswitch_data_46
    .sparse-switch
        -0x5221b369 -> :sswitch_14
        -0x45a505d1 -> :sswitch_45
        -0x4371d164 -> :sswitch_42
        -0x3ca07670 -> :sswitch_11
        -0x238dae5b -> :sswitch_17
        0x1ed28935 -> :sswitch_36
        0x29491feb -> :sswitch_3c
    .end sparse-switch

    :sswitch_data_64
    .sparse-switch
        -0x75edda6b -> :sswitch_2b
        0x27552ac8 -> :sswitch_25
        0x4ab6045e -> :sswitch_33
        0x675efa23 -> :sswitch_30
    .end sparse-switch
.end method

.method public static 岬()Z
    .registers 11

    const/16 v10, 0x12

    const/4 v9, 0x3

    const/4 v3, 0x1

    const/4 v1, 0x0

    const/4 v4, 0x0

    :try_start_6
    sget-object v5, Landroid/os/Build;->SUPPORTED_32_BIT_ABIS:[Ljava/lang/String;

    array-length v6, v5
    :try_end_9
    .catch Ljava/lang/NoSuchFieldError; {:try_start_6 .. :try_end_9} :catch_26b

    move v0, v1

    :goto_a
    const v7, 0x6753f160    # 1.0008719E24f

    const-string v2, "\u06d8\u06d8\u06d8\u06e7\u06dc\u06d8\u06dc\u06d6\u06d6\u06d8\u06e4\u06d7\u06ec\u06e2\u06e1\u06e2\u06d9\u06e1\u06e8\u06dc\u06e5\u06e1\u06db\u06e0\u06e4"

    :goto_f
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v8

    xor-int/2addr v8, v7

    sparse-switch v8, :sswitch_data_40e

    goto :goto_f

    :sswitch_18
    const v2, -0x413f33d3

    :try_start_1b
    const-string v0, "\u06e4\u06e0\u06d7\u06e5\u06db\u06e6\u06da\u06e0\u06e8\u06d8\u06e1\u06da\u06dc\u06e2\u06d8"

    :goto_1d
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v5

    xor-int/2addr v5, v2

    sparse-switch v5, :sswitch_data_420

    goto :goto_1d

    :sswitch_26
    sget-object v0, Landroid/os/Build;->CPU_ABI2:Ljava/lang/String;

    const-string v2, "x86"

    invoke-virtual {v0, v2}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    const v5, -0x26977b50

    const-string v0, "\u06e1\u06e6\u06e5\u06db\u06da\u06e4\u06ec\u06d8\u06e1\u06d8\u06e0\u06e0\u06dc\u06df\u06d7\u06d7\u06e8\u06e1\u06d6\u06e8\u06d7\u06eb\u06dc\u06e2\u06e4\u06e7\u06e5\u06e2"

    :goto_33
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_36
    .catch Ljava/lang/NoSuchFieldError; {:try_start_1b .. :try_end_36} :catch_26b

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_432

    goto :goto_33

    :sswitch_3c
    move v1, v3

    :goto_3d
    :sswitch_3d
    return v1

    :cond_3e
    const-string v2, "\u06ec\u06e5\u06d8\u06d7\u06ec\u06e4\u06d7\u06e2\u06ec\u06da\u06db\u06e8\u06d6\u06d7\u06e1\u06d9\u06da\u06e6\u06ec\u06db\u06da\u06d8\u06db\u06e5"

    goto :goto_f

    :sswitch_41
    if-ge v0, v6, :cond_3e

    const-string v2, "\u06d8\u06e1\u06dc\u06d8\u06e1\u06dc\u06eb\u06e1\u06e8\u06d9\u06dc\u06d8\u06dc\u06e2\u06db\u06e5\u06d8\u06e0\u06e2\u06d6\u06d8"

    goto :goto_f

    :sswitch_46
    const-string v2, "\u06ec\u06ec\u06dc\u06e6\u06e2\u06e7\u06d9\u06db\u06e1\u06d8\u06e8\u06e7\u06d6\u06da\u06df\u06ec\u06e0\u06e2\u06e6\u06dc\u06df\u06eb\u06dc\u06da\u06d8\u06d8"

    goto :goto_f

    :sswitch_49
    const v7, 0xe783550

    :try_start_4c
    const-string v2, "\u06db\u06e2\u06e6\u06e4\u06e8\u06e0\u06d8\u06d8\u06e6\u06ec\u06e2\u06d6\u06ec\u06df\u06e4\u06e0\u06df\u06dc"

    :goto_4e
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v8

    xor-int/2addr v8, v7

    sparse-switch v8, :sswitch_data_444

    goto :goto_4e

    :sswitch_57
    const-string v2, "\u06ec\u06d7\u06e6\u06d8\u06db\u06d6\u06e5\u06e6\u06ec\u06e1\u06dc\u06e7\u06e8\u06d8\u06ec\u06e1\u06e8\u06d8\u06ec\u06e2\u06e1\u06d8"

    goto :goto_4e

    :cond_5a
    const-string v2, "\u06dc\u06da\u06db\u06e5\u06ec\u06ec\u06e7\u06e8\u06df\u06eb\u06da\u06eb\u06da\u06e0\u06d8\u06d8\u06e4\u06e0\u06e5\u06d8\u06e6\u06e8\u06e6\u06d9\u06d8\u06d9\u06e7\u06e0\u06df"

    goto :goto_4e

    :sswitch_5d
    aget-object v2, v5, v0

    const-string v8, "x86"

    invoke-virtual {v2, v8}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    if-eqz v2, :cond_5a

    const-string v2, "\u06e1\u06e2\u06dc\u06d8\u06ec\u06ec\u06d8\u06e7\u06d6\u06d6\u06d8\u06e2\u06df\u06dc\u06d7\u06db\u06ec\u06d8\u06e6\u06d6"

    goto :goto_4e

    :sswitch_6a
    move v1, v3

    goto :goto_3d

    :sswitch_6c
    add-int/lit8 v0, v0, 0x1

    goto :goto_a

    :cond_6f
    const-string v0, "\u06e0\u06d7\u06dc\u06d9\u06db\u06df\u06e7\u06e8\u06e6\u06e0\u06e1\u06e6\u06ec\u06d7\u06d7\u06e8\u06e1\u06d8\u06ec\u06e8\u06db\u06ec\u06d7\u06e6\u06d8"

    goto :goto_1d

    :sswitch_72
    sget-object v0, Landroid/os/Build;->CPU_ABI:Ljava/lang/String;

    const-string v5, "x86"

    invoke-virtual {v0, v5}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-nez v0, :cond_6f

    const-string v0, "\u06d8\u06e5\u06d8\u06d9\u06d8\u06dc\u06d8\u06d6\u06e8\u06da\u06d7\u06e5\u06e6\u06d9\u06e5\u06d8\u06d8\u06ec\u06df\u06e2\u06db\u06ec\u06e7\u06ec\u06db"

    goto :goto_1d

    :sswitch_7f
    const-string v0, "\u06da\u06d7\u06dc\u06d8\u06e2\u06e1\u06d7\u06eb\u06d6\u06df\u06e4\u06e2\u06e0\u06d9\u06d7\u06e6\u06df\u06e6\u06d6\u06d6\u06d8\u06db\u06d8\u06db"

    goto :goto_1d

    :cond_82
    const-string v0, "\u06e1\u06da\u06d7\u06eb\u06d7\u06d9\u06e2\u06eb\u06e1\u06e0\u06e8\u06d7\u06d9\u06da\u06e7\u06eb\u06da\u06e8\u06d8\u06d7\u06e0\u06dc\u06d8\u06df\u06ec\u06df\u06e7\u06e6\u06d6"

    goto :goto_33

    :sswitch_85
    if-nez v2, :cond_82

    const-string v0, "\u06d7\u06d6\u06db\u06ec\u06e1\u06dc\u06d8\u06e6\u06da\u06e6\u06e4\u06db\u06d9\u06e0\u06e4\u06e4\u06d6\u06df\u06e4\u06e8\u06dc\u06dc\u06e6\u06d8"
    :try_end_89
    .catch Ljava/lang/NoSuchFieldError; {:try_start_4c .. :try_end_89} :catch_26b

    goto :goto_33

    :sswitch_8a
    const-string v0, "\u06eb\u06e8\u06d8\u06e2\u06e0\u06d8\u06d8\u06e5\u06e4\u06e0\u06d7\u06dc\u06d6\u06d8\u06ec\u06d7\u06e1\u06eb\u06da\u06d8\u06d8"

    goto :goto_33

    :sswitch_8d
    :try_start_8d
    new-instance v5, Ljava/io/RandomAccessFile;

    const-string v0, "/system/build.prop"

    const-string v2, "r"

    invoke-direct {v5, v0, v2}, Ljava/io/RandomAccessFile;-><init>(Ljava/lang/String;Ljava/lang/String;)V
    :try_end_96
    .catch Ljava/io/FileNotFoundException; {:try_start_8d .. :try_end_96} :catch_214
    .catch Ljava/io/IOException; {:try_start_8d .. :try_end_96} :catch_237
    .catchall {:try_start_8d .. :try_end_96} :catchall_25a

    :try_start_96
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->readLine()Ljava/lang/String;
    :try_end_99
    .catch Ljava/io/FileNotFoundException; {:try_start_96 .. :try_end_99} :catch_3fd
    .catch Ljava/io/IOException; {:try_start_96 .. :try_end_99} :catch_400
    .catchall {:try_start_96 .. :try_end_99} :catchall_3f2

    move-result-object v0

    :goto_9a
    const v6, -0x68e55773

    const-string v2, "\u06e1\u06e0\u06dc\u06d8\u06e1\u06e4\u06e6\u06df\u06d9\u06da\u06e2\u06d6\u06e6\u06d8\u06e4\u06e8\u06e7\u06d8\u06e5\u06e6\u06e6\u06d8\u06ec\u06e7\u06e6\u06d8\u06db\u06d8\u06e5\u06d8\u06d7\u06d8\u06d9"

    :goto_9f
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_456

    goto :goto_9f

    :sswitch_a8
    const-string v2, "\u06d9\u06e1\u06df\u06d9\u06d6\u06e5\u06e6\u06e7\u06d8\u06d9\u06d6\u06dc\u06e1\u06e8\u06e7\u06e5\u06d9\u06e2"

    goto :goto_9f

    :cond_ab
    const-string v2, "\u06e7\u06e1\u06d9\u06ec\u06da\u06e8\u06e8\u06e0\u06d8\u06d6\u06eb\u06d6\u06d7\u06e5\u06e6\u06e0\u06e8\u06dc\u06d8\u06df\u06e2\u06e5"

    goto :goto_9f

    :sswitch_ae
    if-eqz v0, :cond_ab

    const-string v2, "\u06dc\u06eb\u06eb\u06db\u06df\u06d9\u06d8\u06d8\u06d6\u06df\u06ec\u06e0\u06e4\u06e4\u06e1\u06d8\u06dc\u06da\u06d8"

    goto :goto_9f

    :sswitch_b3
    const v6, 0x24de8165

    :try_start_b6
    const-string v2, "\u06e4\u06e7\u06e7\u06d8\u06da\u06dc\u06d8\u06e6\u06e2\u06e0\u06e2\u06ec\u06ec\u06df\u06e0\u06d7\u06da\u06e2\u06e5\u06e7\u06da\u06da\u06e6\u06eb\u06e5\u06d8\u06d7\u06e4\u06e1\u06d8"

    :goto_b8
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_468

    goto :goto_b8

    :sswitch_c1
    const-string v2, "\u06e1\u06d8\u06e8\u06e6\u06eb\u06e4\u06e4\u06db\u06db\u06e0\u06db\u06d6\u06e1\u06d8\u06df\u06e0\u06df\u06d8\u06e5\u06db\u06e1\u06d8\u06ec\u06d9\u06e8\u06d8"

    goto :goto_b8

    :cond_c4
    const-string v2, "\u06e0\u06e8\u06e5\u06d8\u06da\u06e7\u06e4\u06dc\u06e7\u06e0\u06e4\u06e7\u06db\u06e1\u06d8\u06d8\u06e6\u06e5\u06e6\u06d8\u06e0\u06d9\u06dc\u06d8"

    goto :goto_b8

    :sswitch_c7
    const-string v2, "ro.product.cpu.abi"

    invoke-virtual {v0, v2}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    if-eqz v2, :cond_c4

    const-string v2, "\u06e2\u06e0\u06d7\u06d8\u06df\u06db\u06ec\u06da\u06e8\u06e8\u06df\u06e1\u06dc\u06dc\u06dc\u06db\u06e6\u06e6\u06da\u06d8\u06d8\u06d7\u06e6\u06dc\u06d8"

    goto :goto_b8

    :sswitch_d2
    const-string v2, "x86"

    invoke-virtual {v0, v2}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    const v6, 0x5e430405

    const-string v0, "\u06eb\u06da\u06df\u06e5\u06e0\u06d8\u06d8\u06d9\u06d9\u06ec\u06e6\u06e7\u06e4\u06ec\u06d6\u06d6\u06eb\u06e8\u06d7\u06db\u06e5\u06e6"

    :goto_dd
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_e0
    .catch Ljava/io/FileNotFoundException; {:try_start_b6 .. :try_end_e0} :catch_3fd
    .catch Ljava/io/IOException; {:try_start_b6 .. :try_end_e0} :catch_400
    .catchall {:try_start_b6 .. :try_end_e0} :catchall_3f2

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_47a

    goto :goto_dd

    :sswitch_e6
    const-string v0, "\u06d9\u06d8\u06e5\u06e1\u06e2\u06d8\u06db\u06db\u06e5\u06ec\u06df\u06d8\u06e6\u06df\u06dc\u06da\u06ec"

    goto :goto_dd

    :cond_e9
    :try_start_e9
    const-string v0, "\u06e7\u06e0\u06d9\u06e1\u06da\u06d9\u06e4\u06e5\u06d6\u06d8\u06e7\u06ec\u06e8\u06e6\u06d6\u06dc\u06da\u06e2\u06da"

    goto :goto_dd

    :sswitch_ec
    if-eqz v2, :cond_e9

    const-string v0, "\u06dc\u06e2\u06e1\u06d8\u06db\u06dc\u06d8\u06d8\u06e0\u06df\u06e1\u06d8\u06e7\u06eb\u06e6\u06e4\u06da\u06e6\u06e4\u06ec\u06e6\u06e8\u06d8\u06dc\u06d8\u06e1\u06dc\u06e8\u06db\u06e6\u06e1"
    :try_end_f0
    .catch Ljava/io/FileNotFoundException; {:try_start_e9 .. :try_end_f0} :catch_3fd
    .catch Ljava/io/IOException; {:try_start_e9 .. :try_end_f0} :catch_400
    .catchall {:try_start_e9 .. :try_end_f0} :catchall_3f2

    goto :goto_dd

    :sswitch_f1
    :try_start_f1
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_f4
    .catch Ljava/lang/Exception; {:try_start_f1 .. :try_end_f4} :catch_f7
    .catch Ljava/lang/NoSuchFieldError; {:try_start_f1 .. :try_end_f4} :catch_26b

    move v1, v3

    goto/16 :goto_3d

    :catch_f7
    move-exception v0

    move v1, v3

    goto/16 :goto_3d

    :sswitch_fb
    :try_start_fb
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->readLine()Ljava/lang/String;
    :try_end_fe
    .catch Ljava/io/FileNotFoundException; {:try_start_fb .. :try_end_fe} :catch_3fd
    .catch Ljava/io/IOException; {:try_start_fb .. :try_end_fe} :catch_400
    .catchall {:try_start_fb .. :try_end_fe} :catchall_3f2

    move-result-object v0

    goto :goto_9a

    :sswitch_100
    :try_start_100
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_103
    .catch Ljava/lang/Exception; {:try_start_100 .. :try_end_103} :catch_3f6
    .catch Ljava/lang/NoSuchFieldError; {:try_start_100 .. :try_end_103} :catch_26b

    :goto_103
    :sswitch_103
    :try_start_103
    new-instance v2, Ljava/io/FileInputStream;

    const-string v0, "/system/bin/ls"

    invoke-direct {v2, v0}, Ljava/io/FileInputStream;-><init>(Ljava/lang/String;)V
    :try_end_10a
    .catch Ljava/lang/Exception; {:try_start_103 .. :try_end_10a} :catch_3ad
    .catchall {:try_start_103 .. :try_end_10a} :catchall_3d0

    const/16 v0, 0x14

    :try_start_10c
    new-array v4, v0, [B

    const v5, -0x49822858

    const-string v0, "\u06d7\u06df\u06d8\u06e1\u06ec\u06db\u06d9\u06e6\u06eb\u06da\u06e0\u06da\u06db\u06d8\u06d6\u06df\u06d6\u06e6\u06dc\u06ec\u06dc\u06dc\u06d7\u06d8"

    :goto_113
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_48c

    goto :goto_113

    :sswitch_11c
    invoke-virtual {v2, v4}, Ljava/io/FileInputStream;->read([B)I

    move-result v0

    const/16 v6, 0x14

    if-ne v0, v6, :cond_127

    const-string v0, "\u06e8\u06e4\u06e5\u06d8\u06eb\u06d8\u06ec\u06d8\u06d9\u06db\u06e2\u06eb\u06da\u06ec\u06e4\u06d9\u06d8\u06e4\u06d8"

    goto :goto_113

    :cond_127
    const-string v0, "\u06dc\u06e0\u06e8\u06d8\u06e0\u06e8\u06e8\u06e8\u06dc\u06e7\u06d8\u06db\u06d7\u06df\u06e2\u06df\u06d8\u06d8\u06e7\u06e8\u06e1\u06d8\u06e0\u06e0\u06e6"

    goto :goto_113

    :sswitch_12a
    const-string v0, "\u06d6\u06e7\u06d7\u06eb\u06dc\u06d8\u06d8\u06da\u06e1\u06df\u06d7\u06d8\u06db\u06df\u06da\u06d8\u06d8\u06e4\u06e6\u06e0\u06e1\u06df\u06e7\u06e0\u06df\u06e0"

    goto :goto_113

    :sswitch_12d
    const v5, 0x1fa903c1

    const-string v0, "\u06db\u06e2\u06d6\u06d8\u06e2\u06e2\u06df\u06d9\u06d9\u06e5\u06e5\u06e6\u06e5\u06e7\u06e2\u06ec\u06dc\u06ec\u06d6\u06d7\u06d7\u06d8\u06e2\u06e5\u06da"

    :goto_132
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_135
    .catch Ljava/lang/Exception; {:try_start_10c .. :try_end_135} :catch_409
    .catchall {:try_start_10c .. :try_end_135} :catchall_3ef

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_49e

    goto :goto_132

    :sswitch_13b
    const v3, 0x75458088

    const-string v0, "\u06dc\u06eb\u06e8\u06d9\u06e8\u06ec\u06df\u06dc\u06dc\u06d8\u06e0\u06d6\u06d9\u06e1\u06da\u06e8\u06df\u06eb\u06e8\u06d8"

    :goto_140
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v4

    xor-int/2addr v4, v3

    sparse-switch v4, :sswitch_data_4b0

    goto :goto_140

    :sswitch_149
    :try_start_149
    invoke-virtual {v2}, Ljava/io/FileInputStream;->close()V
    :try_end_14c
    .catch Ljava/io/IOException; {:try_start_149 .. :try_end_14c} :catch_14e

    goto/16 :goto_3d

    :catch_14e
    move-exception v0

    goto/16 :goto_3d

    :cond_151
    :try_start_151
    const-string v0, "\u06df\u06d6\u06e6\u06d6\u06d9\u06e1\u06d8\u06da\u06e5\u06e4\u06e5\u06df\u06da\u06e8\u06e5\u06e1\u06e8\u06dc"

    goto :goto_132

    :sswitch_154
    const/4 v0, 0x0

    aget-byte v0, v4, v0

    const/16 v6, 0x7f

    if-ne v0, v6, :cond_151

    const-string v0, "\u06d9\u06e4\u06ec\u06dc\u06d9\u06d8\u06d8\u06d6\u06db\u06da\u06d6\u06d8\u06d8\u06e7\u06e5\u06d7\u06d9\u06d9\u06eb"
    :try_end_15d
    .catch Ljava/lang/Exception; {:try_start_151 .. :try_end_15d} :catch_409
    .catchall {:try_start_151 .. :try_end_15d} :catchall_3ef

    goto :goto_132

    :sswitch_15e
    const-string v0, "\u06da\u06eb\u06d6\u06d8\u06e1\u06e5\u06ec\u06dc\u06e8\u06e5\u06d8\u06ec\u06e6\u06e4\u06d8\u06d8\u06d6\u06d9\u06dc\u06d8"

    goto :goto_132

    :sswitch_161
    const v5, -0x513414d6

    const-string v0, "\u06d7\u06eb\u06dc\u06d8\u06e2\u06ec\u06d8\u06d6\u06d6\u06db\u06e6\u06e7\u06e0\u06d8\u06e4\u06e7\u06e8\u06e8\u06d8\u06d6\u06e1\u06db\u06e0\u06e2\u06dc\u06d8"

    :goto_166
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_4c2

    goto :goto_166

    :sswitch_16f
    const v5, 0x5ea0af52

    const-string v0, "\u06d6\u06e8\u06e5\u06d8\u06eb\u06db\u06e6\u06e7\u06e1\u06d8\u06e0\u06e7\u06e0\u06db\u06e6\u06db\u06ec\u06df\u06d8\u06eb\u06dc\u06df\u06e6\u06da\u06e6\u06d8\u06e2\u06df\u06e0"

    :goto_174
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_4d4

    goto :goto_174

    :sswitch_17d
    const-string v0, "\u06e5\u06d8\u06d7\u06df\u06dc\u06e4\u06d7\u06db\u06dc\u06d8\u06d6\u06d6\u06ec\u06e1\u06da\u06e7\u06d9\u06ec\u06d8\u06d8\u06e1\u06e0\u06db\u06d6\u06eb\u06e1\u06e0\u06e0"

    goto :goto_174

    :cond_180
    const-string v0, "\u06e4\u06ec\u06e4\u06e5\u06e4\u06d7\u06d7\u06e8\u06e6\u06d8\u06eb\u06e7\u06e6\u06d8\u06e7\u06e6\u06e5\u06d8\u06d9\u06da\u06d9"

    goto :goto_166

    :sswitch_183
    aget-byte v0, v4, v3

    const/16 v6, 0x45

    if-ne v0, v6, :cond_180

    const-string v0, "\u06e5\u06e2\u06d9\u06df\u06d7\u06e4\u06e7\u06df\u06ec\u06e2\u06e0\u06e5\u06d8\u06eb\u06db\u06e8\u06d9\u06eb\u06e2\u06e4\u06d8\u06e2\u06e6\u06d9"

    goto :goto_166

    :sswitch_18c
    const-string v0, "\u06d8\u06dc\u06e8\u06df\u06e0\u06d8\u06e8\u06e4\u06e5\u06da\u06d8\u06d7\u06e8\u06e0\u06d8\u06e4\u06e2\u06d8"

    goto :goto_166

    :cond_18f
    const-string v0, "\u06ec\u06e1\u06dc\u06d8\u06e5\u06e4\u06e6\u06d8\u06e7\u06e8\u06d6\u06d8\u06eb\u06d6\u06d7\u06d7\u06eb\u06db\u06e0\u06e6\u06e4\u06dc\u06e1\u06d8\u06e0\u06ec\u06db"

    goto :goto_174

    :sswitch_192
    const/4 v0, 0x2

    aget-byte v0, v4, v0

    const/16 v6, 0x4c

    if-ne v0, v6, :cond_18f

    const-string v0, "\u06d9\u06db\u06d6\u06d8\u06e7\u06e1\u06e2\u06df\u06e8\u06d6\u06d8\u06e5\u06eb\u06dc\u06d8\u06e6\u06d8\u06e1\u06d8\u06d6\u06d8\u06e4\u06db\u06da\u06e5\u06db\u06df\u06e1\u06d8"

    goto :goto_174

    :sswitch_19c
    const v5, -0x2a5fe110

    const-string v0, "\u06dc\u06eb\u06ec\u06d9\u06ec\u06e1\u06d8\u06e0\u06e1\u06e8\u06d8\u06e6\u06d8\u06da\u06dc\u06d6\u06e4"

    :goto_1a1
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_4e6

    goto :goto_1a1

    :sswitch_1aa
    const v5, 0x76f124e4

    const-string v0, "\u06e1\u06d6\u06d8\u06e1\u06d8\u06da\u06e2\u06e1\u06e6\u06d8\u06eb\u06d6\u06e0\u06e1\u06d7\u06d8\u06d8"

    :goto_1af
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_4f8

    goto :goto_1af

    :sswitch_1b8
    aget-byte v0, v4, v10

    if-eq v0, v9, :cond_1ce

    const-string v0, "\u06e7\u06dc\u06d8\u06da\u06e0\u06e0\u06e4\u06ec\u06e1\u06e5\u06e4\u06db\u06df\u06d8\u06e7\u06e4\u06e1\u06e0"

    goto :goto_1af

    :cond_1bf
    const-string v0, "\u06d6\u06e2\u06e6\u06d8\u06e2\u06e6\u06e1\u06d8\u06d8\u06d6\u06d7\u06e8\u06e2\u06e1\u06e0\u06dc\u06d8\u06e8\u06db\u06e6"

    goto :goto_1a1

    :sswitch_1c2
    aget-byte v0, v4, v9

    const/16 v6, 0x46

    if-ne v0, v6, :cond_1bf

    const-string v0, "\u06e5\u06e6\u06e5\u06d8\u06dc\u06e2\u06ec\u06dc\u06d6\u06db\u06d9\u06e4\u06e4\u06e5\u06d8\u06df\u06db\u06d8\u06d9\u06d8\u06e7\u06dc\u06d8\u06dc\u06d6\u06e6"

    goto :goto_1a1

    :sswitch_1cb
    const-string v0, "\u06e5\u06e0\u06e1\u06d8\u06d6\u06dc\u06e5\u06d8\u06e2\u06db\u06d8\u06d8\u06dc\u06e0\u06dc\u06db\u06eb\u06e1\u06d8"

    goto :goto_1a1

    :cond_1ce
    const-string v0, "\u06e6\u06e4\u06e8\u06d8\u06d9\u06d7\u06e4\u06eb\u06e5\u06dc\u06e7\u06e1\u06e5\u06d9\u06e1\u06e1\u06e4\u06e0\u06e1\u06d8\u06e8\u06ec\u06d8\u06e4\u06e1\u06dc"

    goto :goto_1af

    :sswitch_1d1
    const-string v0, "\u06da\u06e4\u06eb\u06e5\u06e4\u06da\u06ec\u06dc\u06e7\u06d8\u06d7\u06e1\u06e5\u06d8\u06d9\u06ec\u06e2"

    goto :goto_1af

    :sswitch_1d4
    aget-byte v4, v4, v10

    const v5, -0x3ad86051

    const-string v0, "\u06df\u06df\u06e6\u06d9\u06e0\u06e4\u06eb\u06d7\u06d8\u06d6\u06e4\u06e8\u06d8\u06dc\u06e7\u06dc\u06dc\u06e8\u06d6"

    :goto_1db
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v5

    sparse-switch v6, :sswitch_data_50a

    goto :goto_1db

    :sswitch_1e4
    const v1, -0x7a361c87

    const-string v0, "\u06e4\u06e2\u06e1\u06d8\u06ec\u06dc\u06db\u06ec\u06e0\u06e5\u06d8\u06db\u06e4\u06d9\u06e7\u06e8\u06e5\u06d8\u06eb\u06d8\u06e1\u06d8\u06e1\u06d7\u06e8\u06e7\u06d8\u06db\u06da\u06e2\u06d8"

    :goto_1e9
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v4

    xor-int/2addr v4, v1

    sparse-switch v4, :sswitch_data_51c

    goto :goto_1e9

    :sswitch_1f2
    if-eqz v2, :cond_204

    const-string v0, "\u06df\u06da\u06db\u06e8\u06d9\u06d8\u06d8\u06e1\u06e1\u06da\u06e2\u06e2\u06e5\u06d8\u06d6\u06e5\u06d8\u06df\u06ec\u06dc\u06eb\u06eb\u06df\u06e7\u06d9"

    goto :goto_1e9

    :cond_1f7
    const-string v0, "\u06df\u06d6\u06e8\u06df\u06db\u06e1\u06d8\u06e2\u06ec\u06e8\u06d7\u06e6\u06e1\u06d8\u06db\u06e6\u06d9\u06eb\u06e2\u06d8\u06d8"

    goto :goto_1db

    :sswitch_1fa
    const/16 v0, 0x3e

    if-ne v4, v0, :cond_1f7

    const-string v0, "\u06dc\u06d8\u06e6\u06d8\u06d9\u06eb\u06e1\u06d8\u06e4\u06df\u06da\u06e0\u06e1\u06d7\u06e5\u06e4\u06e4"

    goto :goto_1db

    :sswitch_201
    const-string v0, "\u06da\u06e8\u06d8\u06e7\u06e0\u06e6\u06db\u06d9\u06e4\u06da\u06d7\u06e5\u06d8\u06d6\u06df\u06da"

    goto :goto_1db

    :cond_204
    const-string v0, "\u06dc\u06e5\u06e1\u06d8\u06e7\u06e0\u06e8\u06d8\u06eb\u06eb\u06ec\u06e1\u06e7\u06db\u06d6\u06e4\u06e7"

    goto :goto_1e9

    :sswitch_207
    const-string v0, "\u06eb\u06e5\u06db\u06e8\u06e5\u06e2\u06e1\u06e2\u06d7\u06d6\u06e6\u06e0\u06d8\u06da\u06d8\u06db\u06df\u06e8\u06d8\u06e7\u06e2\u06e8\u06d8\u06e2\u06e4\u06e8\u06d8\u06df\u06e2\u06da"

    goto :goto_1e9

    :sswitch_20a
    :try_start_20a
    invoke-virtual {v2}, Ljava/io/FileInputStream;->close()V
    :try_end_20d
    .catch Ljava/io/IOException; {:try_start_20a .. :try_end_20d} :catch_210

    move v1, v3

    goto/16 :goto_3d

    :catch_210
    move-exception v0

    move v1, v3

    goto/16 :goto_3d

    :catch_214
    move-exception v0

    move-object v5, v4

    :goto_216
    const v2, 0x7124160d

    const-string v0, "\u06d7\u06d8\u06e2\u06e4\u06e4\u06d8\u06db\u06d6\u06e1\u06d8\u06d6\u06d9\u06d8\u06d8\u06e1\u06e4\u06e5\u06e1\u06e5\u06da\u06db\u06e7\u06e5\u06d8\u06e6\u06dc\u06da"

    :goto_21b
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v2

    sparse-switch v6, :sswitch_data_52e

    goto :goto_21b

    :sswitch_224
    :try_start_224
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_227
    .catch Ljava/lang/Exception; {:try_start_224 .. :try_end_227} :catch_229
    .catch Ljava/lang/NoSuchFieldError; {:try_start_224 .. :try_end_227} :catch_26b

    goto/16 :goto_103

    :catch_229
    move-exception v0

    goto/16 :goto_103

    :cond_22c
    const-string v0, "\u06eb\u06d7\u06d9\u06e2\u06df\u06dc\u06e6\u06e7\u06d7\u06ec\u06ec\u06e5\u06d8\u06e4\u06d6"

    goto :goto_21b

    :sswitch_22f
    if-eqz v5, :cond_22c

    const-string v0, "\u06ec\u06eb\u06e6\u06e7\u06d7\u06e6\u06d8\u06d7\u06ec\u06e5\u06d7\u06e0\u06e1\u06d8\u06e1\u06d9\u06da"

    goto :goto_21b

    :sswitch_234
    const-string v0, "\u06e5\u06d6\u06df\u06e8\u06e0\u06da\u06df\u06df\u06e6\u06d8\u06d9\u06db\u06dc\u06e7\u06e6\u06eb"

    goto :goto_21b

    :catch_237
    move-exception v0

    move-object v5, v4

    :goto_239
    const v2, 0x5d46a890

    const-string v0, "\u06e8\u06e1\u06e1\u06d8\u06d6\u06db\u06e6\u06da\u06ec\u06e6\u06d8\u06d7\u06d6\u06df\u06d8\u06df\u06df\u06e4\u06db\u06d9\u06df\u06d8\u06e1\u06e5\u06e5\u06ec"

    :goto_23e
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v2

    sparse-switch v6, :sswitch_data_540

    goto :goto_23e

    :sswitch_247
    :try_start_247
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_24a
    .catch Ljava/lang/Exception; {:try_start_247 .. :try_end_24a} :catch_24c
    .catch Ljava/lang/NoSuchFieldError; {:try_start_247 .. :try_end_24a} :catch_26b

    goto/16 :goto_103

    :catch_24c
    move-exception v0

    goto/16 :goto_103

    :cond_24f
    const-string v0, "\u06d7\u06e7\u06d9\u06e7\u06eb\u06e4\u06e5\u06d8\u06ec\u06eb\u06e0\u06e8\u06e2\u06e8\u06e8\u06eb\u06eb\u06e8\u06eb\u06dc\u06d8"

    goto :goto_23e

    :sswitch_252
    if-eqz v5, :cond_24f

    const-string v0, "\u06df\u06ec\u06eb\u06d6\u06d7\u06d8\u06d8\u06e4\u06e7\u06d7\u06e0\u06e2\u06dc\u06d8\u06d7\u06ec\u06e6\u06d8\u06eb\u06d6\u06e5\u06d8\u06d6\u06e1\u06e6\u06d8\u06eb\u06eb\u06d7\u06e0\u06ec"

    goto :goto_23e

    :sswitch_257
    const-string v0, "\u06e1\u06da\u06da\u06e1\u06e8\u06e6\u06db\u06eb\u06d7\u06d9\u06e1\u06e1\u06d8\u06e6\u06db\u06d8\u06d8\u06e5\u06e4\u06e4\u06d9\u06eb\u06e8\u06d8\u06e0\u06da\u06dc"

    goto :goto_23e

    :catchall_25a
    move-exception v2

    move-object v0, v4

    :goto_25c
    const v6, 0x7b1b7884

    const-string v5, "\u06da\u06e5\u06d9\u06e4\u06dc\u06e7\u06dc\u06dc\u06e7\u06d8\u06d8\u06ec\u06e4\u06d6\u06e4\u06e1\u06d8"

    :goto_261
    invoke-virtual {v5}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_552

    goto :goto_261

    :goto_26a
    :sswitch_26a
    :try_start_26a
    throw v2

    :catch_26b
    move-exception v0

    const v2, 0x7ec220bb

    const-string v0, "\u06dc\u06e6\u06d6\u06d8\u06e4\u06e5\u06dc\u06d8\u06ec\u06eb\u06e6\u06df\u06e0\u06d9\u06e5\u06da\u06e8\u06dc\u06e0\u06d6\u06e1\u06df\u06d8\u06d9\u06e8\u06e2\u06db\u06df\u06d6"

    :goto_271
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_274
    .catch Ljava/lang/NoSuchFieldError; {:try_start_26a .. :try_end_274} :catch_26b

    move-result v5

    xor-int/2addr v5, v2

    sparse-switch v5, :sswitch_data_564

    goto :goto_271

    :sswitch_27a
    const-string v0, "\u06eb\u06e5\u06e8\u06d8\u06e1\u06dc\u06eb\u06e1\u06d8\u06e2\u06e4\u06e5\u06d7\u06d7\u06e1\u06e7\u06df\u06da"

    goto :goto_271

    :cond_27d
    const-string v5, "\u06e5\u06d6\u06df\u06db\u06e1\u06e0\u06e5\u06e4\u06ec\u06e2\u06e2\u06ec\u06d7\u06e5\u06d7\u06d6\u06db\u06e2\u06e8\u06e1\u06df"

    goto :goto_261

    :sswitch_280
    if-eqz v0, :cond_27d

    const-string v5, "\u06dc\u06df\u06e1\u06d8\u06e0\u06e2\u06e0\u06e0\u06e4\u06db\u06ec\u06e7\u06e0\u06e5\u06d9\u06eb\u06db\u06db\u06e7\u06d8\u06eb\u06dc\u06e1\u06d9\u06db"

    goto :goto_261

    :sswitch_285
    const-string v5, "\u06e7\u06db\u06e1\u06d8\u06da\u06eb\u06d8\u06e5\u06da\u06ec\u06db\u06e1\u06e5\u06d8\u06da\u06dc\u06d8\u06d9\u06d9\u06dc\u06e8\u06eb\u06e5\u06e8\u06e4\u06e8\u06d8"

    goto :goto_261

    :sswitch_288
    :try_start_288
    invoke-virtual {v0}, Ljava/io/RandomAccessFile;->close()V
    :try_end_28b
    .catch Ljava/lang/Exception; {:try_start_288 .. :try_end_28b} :catch_28c
    .catch Ljava/lang/NoSuchFieldError; {:try_start_288 .. :try_end_28b} :catch_26b

    goto :goto_26a

    :catch_28c
    move-exception v0

    goto :goto_26a

    :cond_28e
    :try_start_28e
    const-string v0, "\u06e2\u06e6\u06d8\u06d8\u06dc\u06d7\u06e8\u06d8\u06e1\u06dc\u06db\u06dc\u06e0\u06eb\u06db\u06e0"

    goto :goto_271

    :sswitch_291
    sget-object v0, Landroid/os/Build;->CPU_ABI:Ljava/lang/String;

    const-string v5, "x86"

    invoke-virtual {v0, v5}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-nez v0, :cond_28e

    const-string v0, "\u06ec\u06ec\u06df\u06e7\u06e6\u06ec\u06d6\u06e7\u06ec\u06eb\u06e5\u06d8\u06e7\u06d8\u06dc\u06d8"
    :try_end_29d
    .catch Ljava/lang/NoSuchFieldError; {:try_start_28e .. :try_end_29d} :catch_26b

    goto :goto_271

    :sswitch_29e
    const v2, 0x5761bc7

    const-string v0, "\u06e5\u06da\u06dc\u06e7\u06e0\u06d6\u06d8\u06e8\u06df\u06e7\u06e0\u06e7\u06ec\u06e8\u06e8\u06eb\u06e5\u06e5\u06e2\u06e6\u06e0\u06e6\u06ec\u06d8\u06e7\u06df"

    :goto_2a3
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v5

    xor-int/2addr v5, v2

    sparse-switch v5, :sswitch_data_576

    goto :goto_2a3

    :sswitch_2ac
    const-string v0, "\u06e5\u06dc\u06d9\u06eb\u06df\u06e6\u06db\u06e1\u06e0\u06eb\u06d8\u06df\u06e4\u06d7\u06ec\u06ec\u06d9\u06eb\u06eb\u06e2\u06ec\u06e7\u06ec\u06e6\u06e8\u06e7\u06e7"

    goto :goto_2a3

    :cond_2af
    const-string v0, "\u06d6\u06e2\u06e8\u06e2\u06e0\u06e1\u06d8\u06db\u06e6\u06eb\u06d7\u06e6\u06e1\u06d7\u06d6\u06e6\u06d8\u06eb\u06d8\u06e1\u06ec\u06d7\u06dc\u06e5\u06d8\u06e2\u06d7\u06e1\u06d8"

    goto :goto_2a3

    :sswitch_2b2
    sget-object v0, Landroid/os/Build;->CPU_ABI2:Ljava/lang/String;

    const-string v5, "x86"

    invoke-virtual {v0, v5}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-nez v0, :cond_2af

    const-string v0, "\u06eb\u06d9\u06e4\u06e6\u06e4\u06ec\u06d8\u06e5\u06d8\u06db\u06e5\u06dc\u06e4\u06ec\u06e2\u06e6\u06db\u06e5\u06ec\u06d7\u06df\u06e4\u06e5\u06d6\u06e2\u06dc\u06d6\u06d8"

    goto :goto_2a3

    :sswitch_2bf
    :try_start_2bf
    new-instance v5, Ljava/io/RandomAccessFile;

    const-string v0, "/system/build.prop"

    const-string v2, "r"

    invoke-direct {v5, v0, v2}, Ljava/io/RandomAccessFile;-><init>(Ljava/lang/String;Ljava/lang/String;)V
    :try_end_2c8
    .catch Ljava/io/FileNotFoundException; {:try_start_2bf .. :try_end_2c8} :catch_33a
    .catch Ljava/io/IOException; {:try_start_2bf .. :try_end_2c8} :catch_35d
    .catchall {:try_start_2bf .. :try_end_2c8} :catchall_40b

    :try_start_2c8
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->readLine()Ljava/lang/String;
    :try_end_2cb
    .catch Ljava/io/FileNotFoundException; {:try_start_2c8 .. :try_end_2cb} :catch_403
    .catch Ljava/io/IOException; {:try_start_2c8 .. :try_end_2cb} :catch_406
    .catchall {:try_start_2c8 .. :try_end_2cb} :catchall_380

    move-result-object v0

    :goto_2cc
    const v6, 0x6cd6ee36

    const-string v2, "\u06d8\u06e8\u06ec\u06d9\u06dc\u06d7\u06d7\u06d6\u06e5\u06d7\u06db\u06d8\u06d8\u06e7\u06e6"

    :goto_2d1
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_588

    goto :goto_2d1

    :sswitch_2da
    if-eqz v0, :cond_2df

    const-string v2, "\u06e7\u06e0\u06ec\u06e7\u06df\u06e8\u06d8\u06e0\u06e7\u06d6\u06d8\u06eb\u06e5\u06e5\u06d8\u06d7\u06e8\u06e0\u06e5\u06d9\u06e6\u06d8"

    goto :goto_2d1

    :cond_2df
    const-string v2, "\u06e7\u06d9\u06eb\u06da\u06da\u06e7\u06e1\u06d7\u06e5\u06d8\u06dc\u06d8\u06db\u06dc\u06eb\u06e1\u06d8\u06df\u06df\u06e4\u06e7\u06d7\u06db"

    goto :goto_2d1

    :sswitch_2e2
    const-string v2, "\u06e8\u06e0\u06e8\u06e2\u06db\u06e1\u06e2\u06d9\u06e4\u06e4\u06e0\u06dc\u06e2\u06e8\u06e6\u06dc\u06db\u06e0\u06e7\u06d8\u06e5\u06d8\u06e1\u06ec\u06e2\u06e1\u06e2\u06d7"

    goto :goto_2d1

    :sswitch_2e5
    const v6, 0x26e12e9a

    :try_start_2e8
    const-string v2, "\u06dc\u06d8\u06e1\u06e6\u06d7\u06dc\u06d8\u06d6\u06e4\u06dc\u06e8\u06e5\u06e7\u06d8\u06e1\u06e0\u06e6\u06e0\u06ec\u06e0\u06e2\u06e4\u06d6\u06e4\u06d7\u06db\u06d7\u06e6\u06db"

    :goto_2ea
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_59a

    goto :goto_2ea

    :sswitch_2f3
    const-string v2, "\u06d8\u06e2\u06e4\u06e1\u06d7\u06da\u06e6\u06ec\u06d6\u06e4\u06df\u06d6\u06d8\u06e4\u06db\u06d8\u06e5\u06d7\u06e0\u06d6\u06e1\u06e1"

    goto :goto_2ea

    :cond_2f6
    const-string v2, "\u06ec\u06db\u06d6\u06db\u06ec\u06d6\u06d8\u06e7\u06e6\u06da\u06e4\u06e2\u06e7\u06e0\u06d7\u06e0\u06e6\u06e2\u06e8\u06d8\u06e6\u06e2\u06ec\u06e4\u06e1\u06e4"

    goto :goto_2ea

    :sswitch_2f9
    const-string v2, "ro.product.cpu.abi"

    invoke-virtual {v0, v2}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    if-eqz v2, :cond_2f6

    const-string v2, "\u06d8\u06df\u06d7\u06e2\u06e6\u06df\u06dc\u06db\u06e8\u06d8\u06d9\u06e7\u06db\u06eb\u06df\u06e8\u06d8\u06dc\u06d7\u06d6\u06d8"

    goto :goto_2ea

    :sswitch_304
    const-string v2, "x86"

    invoke-virtual {v0, v2}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    const v6, -0xf03eebc

    const-string v0, "\u06e7\u06d9\u06df\u06eb\u06e5\u06dc\u06d8\u06d9\u06d9\u06d9\u06da\u06da\u06d8\u06d8\u06e4\u06e5\u06e0\u06d9\u06e5\u06e8\u06d8\u06e0\u06e0\u06d9"

    :goto_30f
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_312
    .catch Ljava/io/FileNotFoundException; {:try_start_2e8 .. :try_end_312} :catch_403
    .catch Ljava/io/IOException; {:try_start_2e8 .. :try_end_312} :catch_406
    .catchall {:try_start_2e8 .. :try_end_312} :catchall_380

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_5ac

    goto :goto_30f

    :sswitch_318
    :try_start_318
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_31b
    .catch Ljava/lang/Exception; {:try_start_318 .. :try_end_31b} :catch_329

    move v1, v3

    goto/16 :goto_3d

    :cond_31e
    :try_start_31e
    const-string v0, "\u06e0\u06e5\u06e7\u06e0\u06e5\u06e4\u06dc\u06ec\u06d6\u06eb\u06e6\u06d8\u06dc\u06e5\u06d9\u06e2\u06d9\u06e5\u06ec\u06df\u06da\u06d9\u06d6\u06e7"

    goto :goto_30f

    :sswitch_321
    if-eqz v2, :cond_31e

    const-string v0, "\u06e4\u06db\u06eb\u06e2\u06d8\u06d7\u06dc\u06db\u06e8\u06ec\u06d8\u06dc\u06d8\u06d6\u06db\u06e4"
    :try_end_325
    .catch Ljava/io/FileNotFoundException; {:try_start_31e .. :try_end_325} :catch_403
    .catch Ljava/io/IOException; {:try_start_31e .. :try_end_325} :catch_406
    .catchall {:try_start_31e .. :try_end_325} :catchall_380

    goto :goto_30f

    :sswitch_326
    const-string v0, "\u06db\u06d9\u06eb\u06dc\u06d7\u06e6\u06e0\u06e4\u06ec\u06da\u06d9\u06e6\u06d6\u06d8\u06ec"

    goto :goto_30f

    :catch_329
    move-exception v0

    move v1, v3

    goto/16 :goto_3d

    :sswitch_32d
    :try_start_32d
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->readLine()Ljava/lang/String;
    :try_end_330
    .catch Ljava/io/FileNotFoundException; {:try_start_32d .. :try_end_330} :catch_403
    .catch Ljava/io/IOException; {:try_start_32d .. :try_end_330} :catch_406
    .catchall {:try_start_32d .. :try_end_330} :catchall_380

    move-result-object v0

    goto :goto_2cc

    :sswitch_332
    :try_start_332
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_335
    .catch Ljava/lang/Exception; {:try_start_332 .. :try_end_335} :catch_337

    goto/16 :goto_103

    :catch_337
    move-exception v0

    goto/16 :goto_103

    :catch_33a
    move-exception v0

    move-object v5, v4

    :goto_33c
    const v2, -0x718d956e

    const-string v0, "\u06d8\u06dc\u06d9\u06e7\u06e1\u06e6\u06d9\u06dc\u06e1\u06e1\u06e1\u06df\u06e8\u06db\u06d6\u06ec\u06e2\u06e2"

    :goto_341
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v2

    sparse-switch v6, :sswitch_data_5be

    goto :goto_341

    :sswitch_34a
    if-eqz v5, :cond_34f

    const-string v0, "\u06e4\u06dc\u06e5\u06dc\u06e4\u06d8\u06d7\u06d9\u06d8\u06d9\u06e7\u06dc\u06df\u06dc\u06d6\u06da\u06df"

    goto :goto_341

    :cond_34f
    const-string v0, "\u06ec\u06db\u06e1\u06dc\u06d6\u06ec\u06e1\u06e4\u06e8\u06d8\u06eb\u06e7\u06e5\u06d8\u06d6\u06e1\u06d6\u06d8"

    goto :goto_341

    :sswitch_352
    const-string v0, "\u06e8\u06e5\u06dc\u06d8\u06e6\u06dc\u06d6\u06e2\u06ec\u06eb\u06e4\u06e4\u06e6\u06db\u06d9\u06d9\u06e6\u06d9\u06e1\u06e5\u06e2\u06e7"

    goto :goto_341

    :sswitch_355
    :try_start_355
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_358
    .catch Ljava/lang/Exception; {:try_start_355 .. :try_end_358} :catch_35a

    goto/16 :goto_103

    :catch_35a
    move-exception v0

    goto/16 :goto_103

    :catch_35d
    move-exception v0

    move-object v5, v4

    :goto_35f
    const v2, 0x1052e20f

    const-string v0, "\u06e1\u06e1\u06da\u06eb\u06df\u06e8\u06d8\u06d6\u06eb\u06da\u06ec\u06e0\u06e6\u06e4\u06ec\u06df\u06d6\u06e4\u06e5\u06e5\u06db\u06e1\u06d8"

    :goto_364
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v6

    xor-int/2addr v6, v2

    sparse-switch v6, :sswitch_data_5d0

    goto :goto_364

    :sswitch_36d
    const-string v0, "\u06dc\u06e6\u06d9\u06e7\u06e0\u06d7\u06df\u06d9\u06e6\u06d8\u06d9\u06e4\u06eb\u06eb\u06da\u06e6\u06d8\u06d8\u06dc\u06e1"

    goto :goto_364

    :cond_370
    const-string v0, "\u06e6\u06e6\u06e8\u06d8\u06e2\u06da\u06e4\u06e6\u06eb\u06d7\u06d6\u06d6\u06e7\u06d8\u06da\u06e8\u06e0"

    goto :goto_364

    :sswitch_373
    if-eqz v5, :cond_370

    const-string v0, "\u06d7\u06d9\u06da\u06d9\u06e6\u06e5\u06d8\u06dc\u06e4\u06e1\u06e0\u06d7\u06e6\u06d8\u06da\u06e7\u06dc\u06d6\u06d8\u06d7\u06d6\u06d9\u06eb"

    goto :goto_364

    :sswitch_378
    :try_start_378
    invoke-virtual {v5}, Ljava/io/RandomAccessFile;->close()V
    :try_end_37b
    .catch Ljava/lang/Exception; {:try_start_378 .. :try_end_37b} :catch_37d

    goto/16 :goto_103

    :catch_37d
    move-exception v0

    goto/16 :goto_103

    :catchall_380
    move-exception v0

    move-object v4, v5

    :goto_382
    const v2, 0x5dd4f0a3

    const-string v1, "\u06e0\u06e1\u06e5\u06d8\u06d7\u06dc\u06e1\u06d8\u06d8\u06d9\u06d6\u06d8\u06e5\u06dc\u06e0\u06e7\u06d6\u06e8\u06d8\u06e1\u06d6\u06d8\u06d9\u06e6\u06dc\u06d8\u06e2\u06dc\u06ec\u06df\u06e2\u06e6"

    :goto_387
    invoke-virtual {v1}, Ljava/lang/String;->hashCode()I

    move-result v3

    xor-int/2addr v3, v2

    sparse-switch v3, :sswitch_data_5e2

    goto :goto_387

    :sswitch_390
    if-eqz v4, :cond_395

    const-string v1, "\u06e0\u06e8\u06e1\u06d8\u06e0\u06d7\u06d8\u06db\u06e6\u06e5\u06d8\u06ec\u06d9\u06e1\u06d8\u06ec\u06e0\u06e1\u06e0\u06db\u06d6"

    goto :goto_387

    :cond_395
    const-string v1, "\u06df\u06e1\u06d8\u06e2\u06e0\u06d6\u06e4\u06d6\u06e2\u06da\u06ec\u06e5\u06ec\u06e0\u06e1\u06e7\u06e2\u06dc\u06d8"

    goto :goto_387

    :sswitch_398
    const-string v1, "\u06d8\u06e7\u06e5\u06d8\u06dc\u06d9\u06dc\u06eb\u06e6\u06e1\u06d8\u06db\u06e2\u06e7\u06e5\u06e5\u06e5\u06df\u06e6\u06e6\u06d8"

    goto :goto_387

    :sswitch_39b
    :try_start_39b
    invoke-virtual {v4}, Ljava/io/RandomAccessFile;->close()V
    :try_end_39e
    .catch Ljava/lang/Exception; {:try_start_39b .. :try_end_39e} :catch_3f9

    :goto_39e
    :sswitch_39e
    throw v0

    :cond_39f
    const-string v0, "\u06d8\u06e6\u06e1\u06d8\u06dc\u06dc\u06eb\u06d7\u06dc\u06eb\u06db\u06e2\u06e0\u06e6\u06e2\u06e5\u06eb\u06e4\u06e8"

    goto/16 :goto_140

    :sswitch_3a3
    if-eqz v2, :cond_39f

    const-string v0, "\u06eb\u06e2\u06e8\u06e8\u06df\u06ec\u06d6\u06df\u06d9\u06d9\u06d6\u06e6\u06d8\u06db\u06eb\u06db\u06e0\u06e5\u06e6\u06d8\u06e0\u06d6\u06d8\u06e2\u06db\u06e0\u06e7\u06e0\u06e5"

    goto/16 :goto_140

    :sswitch_3a9
    const-string v0, "\u06d9\u06e2\u06d6\u06d8\u06e5\u06e4\u06e1\u06d8\u06e4\u06e5\u06da\u06e8\u06eb\u06e6\u06d8\u06e1\u06e5\u06db\u06e1\u06dc\u06d9\u06db\u06e8\u06e5\u06d8\u06e0\u06e0\u06df"

    goto/16 :goto_140

    :catch_3ad
    move-exception v0

    move-object v2, v4

    :goto_3af
    const v3, -0x7ea47478

    const-string v0, "\u06df\u06d6\u06dc\u06d8\u06e7\u06e2\u06eb\u06df\u06d7\u06e8\u06db\u06eb\u06d6\u06d8\u06dc\u06e0\u06d6\u06d8\u06d8\u06eb\u06e1"

    :goto_3b4
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v4

    xor-int/2addr v4, v3

    sparse-switch v4, :sswitch_data_5f4

    goto :goto_3b4

    :sswitch_3bd
    :try_start_3bd
    invoke-virtual {v2}, Ljava/io/FileInputStream;->close()V
    :try_end_3c0
    .catch Ljava/io/IOException; {:try_start_3bd .. :try_end_3c0} :catch_3c2

    goto/16 :goto_3d

    :catch_3c2
    move-exception v0

    goto/16 :goto_3d

    :cond_3c5
    const-string v0, "\u06e8\u06df\u06eb\u06e4\u06e8\u06eb\u06e1\u06d9\u06e5\u06e4\u06db\u06ec\u06e8\u06d6\u06e8\u06e0\u06d6\u06d8\u06dc\u06dc\u06ec\u06dc\u06e6\u06da"

    goto :goto_3b4

    :sswitch_3c8
    if-eqz v2, :cond_3c5

    const-string v0, "\u06e2\u06e8\u06d9\u06dc\u06db\u06e2\u06dc\u06d8\u06e7\u06d8\u06e6\u06e2\u06e6\u06d8\u06d8\u06e4\u06e2\u06e5\u06d9\u06d7"

    goto :goto_3b4

    :sswitch_3cd
    const-string v0, "\u06dc\u06db\u06d6\u06d7\u06e5\u06ec\u06e6\u06e8\u06dc\u06d8\u06db\u06dc\u06e5\u06d6\u06d8"

    goto :goto_3b4

    :catchall_3d0
    move-exception v0

    move-object v1, v4

    :goto_3d2
    const v3, 0x364bb17

    const-string v2, "\u06da\u06ec\u06eb\u06d8\u06ec\u06e6\u06df\u06da\u06e5\u06d8\u06e5\u06e2\u06da\u06e2\u06d7\u06e8\u06d6\u06d7\u06e5\u06d8\u06dc\u06df\u06da\u06e2\u06d9\u06e1\u06d8"

    :goto_3d7
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v4

    xor-int/2addr v4, v3

    sparse-switch v4, :sswitch_data_606

    goto :goto_3d7

    :sswitch_3e0
    if-eqz v1, :cond_3e5

    const-string v2, "\u06df\u06eb\u06e5\u06e1\u06eb\u06d8\u06d8\u06e1\u06d7\u06d8\u06d8\u06e0\u06d9\u06d6\u06e1\u06dc\u06e5\u06df\u06e4"

    goto :goto_3d7

    :cond_3e5
    const-string v2, "\u06e5\u06dc\u06da\u06dc\u06e8\u06e4\u06da\u06e7\u06d8\u06d8\u06e5\u06da\u06e1\u06d8\u06eb\u06d6\u06e8\u06e7\u06e1"

    goto :goto_3d7

    :sswitch_3e8
    const-string v2, "\u06e1\u06df\u06d9\u06e4\u06e1\u06e8\u06d8\u06e0\u06e0\u06e5\u06d7\u06d6\u06d6\u06ec\u06d7\u06e2"

    goto :goto_3d7

    :sswitch_3eb
    :try_start_3eb
    invoke-virtual {v1}, Ljava/io/FileInputStream;->close()V
    :try_end_3ee
    .catch Ljava/io/IOException; {:try_start_3eb .. :try_end_3ee} :catch_3fb

    :goto_3ee
    :sswitch_3ee
    throw v0

    :catchall_3ef
    move-exception v0

    move-object v1, v2

    goto :goto_3d2

    :catchall_3f2
    move-exception v2

    move-object v0, v5

    goto/16 :goto_25c

    :catch_3f6
    move-exception v0

    goto/16 :goto_103

    :catch_3f9
    move-exception v1

    goto :goto_39e

    :catch_3fb
    move-exception v1

    goto :goto_3ee

    :catch_3fd
    move-exception v0

    goto/16 :goto_216

    :catch_400
    move-exception v0

    goto/16 :goto_239

    :catch_403
    move-exception v0

    goto/16 :goto_33c

    :catch_406
    move-exception v0

    goto/16 :goto_35f

    :catch_409
    move-exception v0

    goto :goto_3af

    :catchall_40b
    move-exception v0

    goto/16 :goto_382

    :sswitch_data_40e
    .sparse-switch
        -0x6d3019f7 -> :sswitch_46
        -0x590dd42a -> :sswitch_41
        -0x3e9d22c6 -> :sswitch_49
        0x788d1d12 -> :sswitch_18
    .end sparse-switch

    :sswitch_data_420
    .sparse-switch
        -0x23bae704 -> :sswitch_3c
        0x239bc9d5 -> :sswitch_7f
        0x53065065 -> :sswitch_26
        0x7335d283 -> :sswitch_72
    .end sparse-switch

    :sswitch_data_432
    .sparse-switch
        0xb256620 -> :sswitch_85
        0x2257ae52 -> :sswitch_8a
        0x27c20846 -> :sswitch_8d
        0x3575fcb9 -> :sswitch_3c
    .end sparse-switch

    :sswitch_data_444
    .sparse-switch
        -0x6d3df04d -> :sswitch_5d
        -0x442abb1b -> :sswitch_6c
        0x25033c03 -> :sswitch_57
        0x5c58cceb -> :sswitch_6a
    .end sparse-switch

    :sswitch_data_456
    .sparse-switch
        -0x2c8009b1 -> :sswitch_100
        0xa964a -> :sswitch_b3
        0x1246f660 -> :sswitch_a8
        0x6b6aa478 -> :sswitch_ae
    .end sparse-switch

    :sswitch_data_468
    .sparse-switch
        -0x437fbf1b -> :sswitch_d2
        0x11a30a5e -> :sswitch_c1
        0x29e2f179 -> :sswitch_c7
        0x4ceb996d -> :sswitch_fb
    .end sparse-switch

    :sswitch_data_47a
    .sparse-switch
        -0x564f8b6c -> :sswitch_e6
        -0x40fba1b7 -> :sswitch_ec
        -0x40f5845f -> :sswitch_f1
        0x272054e3 -> :sswitch_fb
    .end sparse-switch

    :sswitch_data_48c
    .sparse-switch
        -0x746083ab -> :sswitch_11c
        -0x3be38456 -> :sswitch_12d
        0x1f97937 -> :sswitch_13b
        0x7bd3607a -> :sswitch_12a
    .end sparse-switch

    :sswitch_data_49e
    .sparse-switch
        -0x7289d130 -> :sswitch_15e
        -0xdd208b8 -> :sswitch_154
        0x27c6e809 -> :sswitch_13b
        0x5cd07334 -> :sswitch_161
    .end sparse-switch

    :sswitch_data_4b0
    .sparse-switch
        0x4cd46d -> :sswitch_3a3
        0x376c0d08 -> :sswitch_3a9
        0x3cb859a3 -> :sswitch_149
        0x7d3c1237 -> :sswitch_3d
    .end sparse-switch

    :sswitch_data_4c2
    .sparse-switch
        -0x4cd2dee9 -> :sswitch_16f
        -0x3345f09b -> :sswitch_183
        -0x12906622 -> :sswitch_18c
        0x575c3533 -> :sswitch_13b
    .end sparse-switch

    :sswitch_data_4d4
    .sparse-switch
        -0x7d652c46 -> :sswitch_19c
        -0x10494198 -> :sswitch_13b
        0x1ebc81a2 -> :sswitch_192
        0x77c0952b -> :sswitch_17d
    .end sparse-switch

    :sswitch_data_4e6
    .sparse-switch
        -0x7dc9ee49 -> :sswitch_1cb
        -0x62db74b6 -> :sswitch_1c2
        0x192ece -> :sswitch_13b
        0x168d2a6b -> :sswitch_1aa
    .end sparse-switch

    :sswitch_data_4f8
    .sparse-switch
        -0x7da11655 -> :sswitch_1d1
        -0x389a60ae -> :sswitch_1e4
        -0x175f3bad -> :sswitch_1d4
        -0x247f542 -> :sswitch_1b8
    .end sparse-switch

    :sswitch_data_50a
    .sparse-switch
        -0x4fb6502f -> :sswitch_1e4
        -0xc4c2688 -> :sswitch_201
        0x65e6e63 -> :sswitch_1fa
        0x54b0a48a -> :sswitch_13b
    .end sparse-switch

    :sswitch_data_51c
    .sparse-switch
        -0x5ba74fea -> :sswitch_207
        -0x2312f482 -> :sswitch_3c
        -0xcc378c -> :sswitch_1f2
        0x5e4a5017 -> :sswitch_20a
    .end sparse-switch

    :sswitch_data_52e
    .sparse-switch
        -0x7f124698 -> :sswitch_22f
        -0x276e6a8b -> :sswitch_224
        0x8ceb276 -> :sswitch_234
        0x3b86dda4 -> :sswitch_103
    .end sparse-switch

    :sswitch_data_540
    .sparse-switch
        -0x3878998 -> :sswitch_247
        0x47698a00 -> :sswitch_103
        0x5e8831e9 -> :sswitch_252
        0x75de05fe -> :sswitch_257
    .end sparse-switch

    :sswitch_data_552
    .sparse-switch
        -0x60bfbb28 -> :sswitch_285
        0x1f930983 -> :sswitch_26a
        0x3fbbc7b0 -> :sswitch_288
        0x4ecc4b67 -> :sswitch_280
    .end sparse-switch

    :sswitch_data_564
    .sparse-switch
        -0x6b28eea4 -> :sswitch_29e
        -0x40b4669b -> :sswitch_27a
        -0x23dc19a5 -> :sswitch_291
        0x76a1bae0 -> :sswitch_3c
    .end sparse-switch

    :sswitch_data_576
    .sparse-switch
        -0x72c860f8 -> :sswitch_2bf
        -0x47484449 -> :sswitch_3c
        0x59da6ed5 -> :sswitch_2ac
        0x79a84a45 -> :sswitch_2b2
    .end sparse-switch

    :sswitch_data_588
    .sparse-switch
        -0x6222e75d -> :sswitch_332
        -0x478a108e -> :sswitch_2e2
        -0x439875e7 -> :sswitch_2e5
        -0x206e3fb9 -> :sswitch_2da
    .end sparse-switch

    :sswitch_data_59a
    .sparse-switch
        -0x34e70632 -> :sswitch_2f3
        -0x19c47545 -> :sswitch_2f9
        0x185c207e -> :sswitch_32d
        0x562e8ebc -> :sswitch_304
    .end sparse-switch

    :sswitch_data_5ac
    .sparse-switch
        -0x7e4cbcf7 -> :sswitch_318
        -0x41af3701 -> :sswitch_326
        0x65750f1 -> :sswitch_32d
        0x42097810 -> :sswitch_321
    .end sparse-switch

    :sswitch_data_5be
    .sparse-switch
        -0x63b3f9ed -> :sswitch_34a
        -0x4d2a30c3 -> :sswitch_103
        0x8a87711 -> :sswitch_352
        0x59380af9 -> :sswitch_355
    .end sparse-switch

    :sswitch_data_5d0
    .sparse-switch
        0x27e93a58 -> :sswitch_378
        0x5bb86a24 -> :sswitch_103
        0x65032e37 -> :sswitch_373
        0x65383037 -> :sswitch_36d
    .end sparse-switch

    :sswitch_data_5e2
    .sparse-switch
        -0x33ef41b5 -> :sswitch_390
        -0x2db46eaf -> :sswitch_398
        0x2c66732e -> :sswitch_39b
        0x42f532fc -> :sswitch_39e
    .end sparse-switch

    :sswitch_data_5f4
    .sparse-switch
        -0x71a7aaf1 -> :sswitch_3d
        -0x3f6c957 -> :sswitch_3bd
        0x11c69b6b -> :sswitch_3c8
        0x79b68030 -> :sswitch_3cd
    .end sparse-switch

    :sswitch_data_606
    .sparse-switch
        -0x6a899876 -> :sswitch_3eb
        -0x1da24784 -> :sswitch_3e8
        0x38a1da9e -> :sswitch_3ee
        0x58ec3be3 -> :sswitch_3e0
    .end sparse-switch
.end method

.method public static 岬(Landroid/content/Context;)Z
    .registers 6

    const/4 v1, 0x1

    :try_start_1
    const-string v0, "q~tb\u007fyt>q``>QsdyfydiDxbuqt"

    invoke-static {v0}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    const-string v2, "sebbu~dQsdyfydiDxbuqt"

    invoke-static {v2}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    const/4 v3, 0x0

    new-array v3, v3, [Ljava/lang/Class;

    invoke-virtual {v0, v2, v3}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v2

    const/4 v3, 0x1

    invoke-virtual {v2, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    const/4 v3, 0x0

    const/4 v4, 0x0

    new-array v4, v4, [Ljava/lang/Object;

    invoke-virtual {v2, v3, v4}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    const-string v3, "wud@b\u007fsucc^q}u"

    invoke-static {v3}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    const/4 v4, 0x0

    new-array v4, v4, [Ljava/lang/Class;

    invoke-virtual {v0, v3, v4}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    const/4 v3, 0x1

    invoke-virtual {v0, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    const/4 v3, 0x0

    new-array v3, v3, [Ljava/lang/Object;

    invoke-virtual {v0, v2, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    invoke-virtual {p0}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v2, v0}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z
    :try_end_45
    .catch Ljava/lang/Throwable; {:try_start_1 .. :try_end_45} :catch_47

    move-result v0

    :goto_46
    return v0

    :catch_47
    move-exception v0

    move v0, v1

    goto :goto_46
.end method

.method public static 岬(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z
    .registers 15

    const/4 v1, 0x0

    const/4 v2, 0x1

    const/4 v3, 0x0

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v4, "/"

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    new-instance v5, Ljava/io/File;

    invoke-direct {v5, p2}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    const v6, 0xd0f41d4

    const-string v0, "\u06eb\u06df\u06d8\u06e4\u06e1\u06dc\u06d8\u06e4\u06ec\u06e6\u06d8\u06e6\u06e8\u06e7\u06d8\u06e7\u06dc\u06da\u06dc\u06e8\u06d8\u06e4\u06e5\u06d6\u06e0\u06e0\u06dc\u06d8"

    :goto_24
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_146

    goto :goto_24

    :sswitch_2d
    new-instance v6, Ljava/io/File;

    invoke-direct {v6, v4}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    :try_start_32
    invoke-virtual {v6}, Ljava/io/File;->exists()Z

    move-result v4

    const v5, -0x4d3e2cbe

    const-string v0, "\u06dc\u06e6\u06e5\u06d8\u06d7\u06db\u06e8\u06d8\u06e0\u06dc\u06dc\u06dc\u06d7\u06e1\u06eb\u06e1\u06dc\u06ec\u06d8\u06e8\u06d8"

    :goto_3b
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_3e
    .catch Ljava/lang/Exception; {:try_start_32 .. :try_end_3e} :catch_113
    .catchall {:try_start_32 .. :try_end_3e} :catchall_12c

    move-result v7

    xor-int/2addr v7, v5

    sparse-switch v7, :sswitch_data_158

    goto :goto_3b

    :sswitch_44
    :try_start_44
    invoke-virtual {p0}, Landroid/content/Context;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    invoke-virtual {v0}, Landroid/content/res/Resources;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v0

    invoke-virtual {v0, p1}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;
    :try_end_4f
    .catchall {:try_start_44 .. :try_end_4f} :catchall_109

    move-result-object v4

    :try_start_50
    new-instance v5, Ljava/io/FileInputStream;

    invoke-direct {v5, v6}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    const v7, -0x35fae29c    # -2180953.0f

    const-string v0, "\u06db\u06da\u06e5\u06e8\u06e5\u06d8\u06d8\u06d8\u06e8\u06e1\u06d8\u06e1\u06da\u06e1\u06d6\u06d9\u06eb\u06ec\u06dc\u06eb\u06d6\u06e6\u06dc\u06df\u06ec\u06e1\u06d8\u06da\u06e2\u06d9"

    :goto_5a
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_5d
    .catchall {:try_start_50 .. :try_end_5d} :catchall_13d

    move-result v8

    xor-int/2addr v8, v7

    sparse-switch v8, :sswitch_data_16a

    goto :goto_5a

    :sswitch_63
    :try_start_63
    invoke-static {v6}, Lv/m/岬;->岬(Ljava/io/File;)V
    :try_end_66
    .catchall {:try_start_63 .. :try_end_66} :catchall_141

    :try_start_66
    invoke-static {v5}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v4}, Lv/m/岬;->岬(Ljava/io/Closeable;)V
    :try_end_6c
    .catch Ljava/lang/Exception; {:try_start_66 .. :try_end_6c} :catch_113
    .catchall {:try_start_66 .. :try_end_6c} :catchall_12c

    invoke-static {v3}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v3}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    move v0, v2

    :goto_73
    return v0

    :cond_74
    const-string v0, "\u06ec\u06e2\u06e0\u06e5\u06ec\u06da\u06db\u06e7\u06e5\u06d6\u06e1\u06e2\u06dc\u06df\u06dc\u06d9\u06e7\u06d8\u06d8\u06df\u06e7\u06d8\u06da\u06d7\u06e2"

    goto :goto_24

    :sswitch_77
    invoke-virtual {v5}, Ljava/io/File;->exists()Z

    move-result v0

    if-nez v0, :cond_74

    const-string v0, "\u06e0\u06e8\u06ec\u06d7\u06d8\u06d7\u06e6\u06ec\u06e0\u06e5\u06e2\u06e8\u06e7\u06d9\u06e5\u06e2\u06e2\u06e8\u06d8\u06e0"

    goto :goto_24

    :sswitch_80
    const-string v0, "\u06df\u06e4\u06d7\u06da\u06e4\u06dc\u06e7\u06ec\u06d9\u06df\u06e0\u06dc\u06d8\u06e8\u06e2\u06e2\u06e5\u06d8\u06e5\u06d8\u06db\u06e7\u06e7"

    goto :goto_24

    :sswitch_83
    const v6, 0x4deb3664    # 4.93276288E8f

    const-string v0, "\u06e4\u06e8\u06e5\u06d8\u06da\u06ec\u06e4\u06e7\u06d8\u06e5\u06d8\u06e2\u06e2\u06e8\u06d6\u06e0\u06dc\u06d8\u06e0\u06eb\u06e6\u06d8\u06e4\u06da\u06d6\u06d8\u06d7\u06e7\u06e6\u06df\u06d9\u06e6\u06d8"

    :goto_88
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_17c

    goto :goto_88

    :sswitch_91
    move v0, v1

    goto :goto_73

    :cond_93
    const-string v0, "\u06ec\u06e0\u06e6\u06e1\u06e6\u06d6\u06e6\u06eb\u06e2\u06df\u06e0\u06d8\u06d6\u06d8\u06e2\u06d9\u06e4\u06db\u06eb\u06e8\u06e6\u06e8\u06e2\u06e4\u06d7\u06e1"

    goto :goto_88

    :sswitch_96
    invoke-virtual {v5}, Ljava/io/File;->mkdirs()Z

    move-result v0

    if-nez v0, :cond_93

    const-string v0, "\u06e0\u06db\u06d8\u06e8\u06e7\u06e5\u06db\u06e4\u06e1\u06d8\u06dc\u06d8\u06dc\u06da\u06e2\u06df\u06e4\u06e5\u06db\u06d8\u06e6\u06d6"

    goto :goto_88

    :sswitch_9f
    const-string v0, "\u06d7\u06ec\u06d8\u06d8\u06d9\u06e5\u06e1\u06db\u06e7\u06e7\u06d9\u06d8\u06e6\u06e7\u06da\u06df"

    goto :goto_88

    :cond_a2
    :try_start_a2
    const-string v0, "\u06da\u06e8\u06e7\u06d9\u06e5\u06e8\u06e0\u06ec\u06e5\u06d7\u06e6\u06e6\u06e2\u06e5\u06d8\u06d8\u06e4\u06dc\u06e2"

    goto :goto_3b

    :sswitch_a5
    if-eqz v4, :cond_a2

    const-string v0, "\u06d6\u06e7\u06e6\u06eb\u06e4\u06e4\u06e2\u06db\u06d9\u06e8\u06e5\u06ec\u06df\u06e0\u06e0\u06db\u06d8\u06e6\u06e6\u06e4\u06db\u06db\u06df\u06d8\u06e6\u06eb\u06e5\u06d8"
    :try_end_a9
    .catch Ljava/lang/Exception; {:try_start_a2 .. :try_end_a9} :catch_113
    .catchall {:try_start_a2 .. :try_end_a9} :catchall_12c

    goto :goto_3b

    :sswitch_aa
    const-string v0, "\u06d6\u06e8\u06e4\u06ec\u06e1\u06d7\u06e2\u06e0\u06d6\u06d6\u06e7\u06d6\u06ec\u06da\u06e8\u06eb\u06e8\u06d8\u06d6\u06d7"

    goto :goto_3b

    :cond_ad
    :try_start_ad
    const-string v0, "\u06e8\u06e4\u06da\u06d9\u06ec\u06e2\u06d7\u06df\u06d8\u06d8\u06ec\u06e6\u06e6\u06e6\u06e8\u06d9\u06d8\u06df\u06d7\u06df\u06da\u06eb\u06da\u06e1"

    goto :goto_5a

    :sswitch_b0
    invoke-static {v4, v5}, Lv/m/岬;->岬(Ljava/io/InputStream;Ljava/io/InputStream;)Z

    move-result v0

    if-eqz v0, :cond_ad

    const-string v0, "\u06d8\u06e7\u06e5\u06d8\u06e7\u06e8\u06e5\u06d8\u06e1\u06e5\u06d8\u06dc\u06e1\u06d9\u06e4\u06db\u06d8\u06e2\u06d8\u06d9"
    :try_end_b8
    .catchall {:try_start_ad .. :try_end_b8} :catchall_13d

    goto :goto_5a

    :sswitch_b9
    :try_start_b9
    const-string v0, "\u06dc\u06d8\u06e7\u06db\u06d7\u06e6\u06e2\u06d8\u06e1\u06dc\u06df\u06e8\u06e5\u06e1\u06e6\u06d8\u06e4\u06ec\u06d9\u06d8\u06e0\u06e2"
    :try_end_bb
    .catchall {:try_start_b9 .. :try_end_bb} :catchall_141

    goto :goto_5a

    :sswitch_bc
    :try_start_bc
    invoke-static {v5}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v4}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    const/4 v0, 0x1

    const/4 v4, 0x1

    invoke-virtual {v6, v0, v4}, Ljava/io/File;->setWritable(ZZ)Z

    :sswitch_c7
    invoke-virtual {p0}, Landroid/content/Context;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    invoke-virtual {v0}, Landroid/content/res/Resources;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v0

    invoke-virtual {v0, p1}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;
    :try_end_d2
    .catch Ljava/lang/Exception; {:try_start_bc .. :try_end_d2} :catch_113
    .catchall {:try_start_bc .. :try_end_d2} :catchall_12c

    move-result-object v4

    :try_start_d3
    new-instance v0, Ljava/io/FileOutputStream;

    invoke-direct {v0, v6}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    :try_end_d8
    .catch Ljava/lang/Exception; {:try_start_d3 .. :try_end_d8} :catch_139
    .catchall {:try_start_d3 .. :try_end_d8} :catchall_136

    const/16 v5, 0x1c00

    :try_start_da
    new-array v7, v5, [B

    :goto_dc
    invoke-virtual {v4, v7}, Ljava/io/InputStream;->read([B)I

    move-result v8

    const v9, 0x29e90d9

    const-string v5, "\u06df\u06e1\u06d9\u06e4\u06e5\u06d6\u06d8\u06e2\u06e7\u06da\u06e7\u06d8\u06e8\u06d7\u06e6\u06db\u06df\u06ec"

    :goto_e5
    invoke-virtual {v5}, Ljava/lang/String;->hashCode()I

    move-result v10

    xor-int/2addr v10, v9

    sparse-switch v10, :sswitch_data_18e

    goto :goto_e5

    :sswitch_ee
    const/4 v5, 0x0

    invoke-virtual {v0, v7, v5, v8}, Ljava/io/FileOutputStream;->write([BII)V
    :try_end_f2
    .catch Ljava/lang/Exception; {:try_start_da .. :try_end_f2} :catch_f3
    .catchall {:try_start_da .. :try_end_f2} :catchall_144

    goto :goto_dc

    :catch_f3
    move-exception v2

    move-object v2, v4

    :goto_f5
    invoke-static {v0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v2}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    move v0, v1

    goto/16 :goto_73

    :cond_fe
    :try_start_fe
    const-string v5, "\u06e7\u06ec\u06d9\u06e5\u06e7\u06e1\u06d8\u06eb\u06d9\u06e6\u06e6\u06d7\u06da\u06e0\u06da\u06d6\u06e5\u06d9\u06eb"

    goto :goto_e5

    :sswitch_101
    if-lez v8, :cond_fe

    const-string v5, "\u06eb\u06dc\u06dc\u06d8\u06e4\u06df\u06e8\u06e2\u06e7\u06d8\u06d8\u06d9\u06e1\u06d8\u06db\u06e0\u06e8\u06e6\u06d9\u06eb\u06d8\u06e4\u06dc\u06d8\u06e2\u06e5"
    :try_end_105
    .catch Ljava/lang/Exception; {:try_start_fe .. :try_end_105} :catch_f3
    .catchall {:try_start_fe .. :try_end_105} :catchall_144

    goto :goto_e5

    :sswitch_106
    const-string v5, "\u06ec\u06df\u06eb\u06ec\u06d9\u06e2\u06e2\u06dc\u06d9\u06e8\u06db\u06e1\u06e5\u06e1\u06db\u06db\u06db\u06e5\u06d8"

    goto :goto_e5

    :catchall_109
    move-exception v0

    move-object v2, v3

    move-object v5, v3

    :goto_10c
    :try_start_10c
    invoke-static {v5}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v2}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    throw v0
    :try_end_113
    .catch Ljava/lang/Exception; {:try_start_10c .. :try_end_113} :catch_113
    .catchall {:try_start_10c .. :try_end_113} :catchall_12c

    :catch_113
    move-exception v0

    move-object v0, v3

    move-object v2, v3

    goto :goto_f5

    :sswitch_117
    :try_start_117
    invoke-virtual {v0}, Ljava/io/FileOutputStream;->flush()V

    invoke-static {v0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v4}, Lv/m/岬;->岬(Ljava/io/Closeable;)V
    :try_end_120
    .catch Ljava/lang/Exception; {:try_start_117 .. :try_end_120} :catch_f3
    .catchall {:try_start_117 .. :try_end_120} :catchall_144

    :try_start_120
    invoke-static {v6}, Lv/m/岬;->岬(Ljava/io/File;)V
    :try_end_123
    .catch Ljava/lang/Exception; {:try_start_120 .. :try_end_123} :catch_113
    .catchall {:try_start_120 .. :try_end_123} :catchall_12c

    invoke-static {v3}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v3}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    move v0, v2

    goto/16 :goto_73

    :catchall_12c
    move-exception v1

    move-object v0, v3

    move-object v4, v3

    :goto_12f
    invoke-static {v0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {v4}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    throw v1

    :catchall_136
    move-exception v1

    move-object v0, v3

    goto :goto_12f

    :catch_139
    move-exception v0

    move-object v0, v3

    move-object v2, v4

    goto :goto_f5

    :catchall_13d
    move-exception v0

    move-object v2, v4

    move-object v5, v3

    goto :goto_10c

    :catchall_141
    move-exception v0

    move-object v2, v4

    goto :goto_10c

    :catchall_144
    move-exception v1

    goto :goto_12f

    :sswitch_data_146
    .sparse-switch
        -0x32758536 -> :sswitch_83
        -0x270f0f6c -> :sswitch_80
        0x46f24314 -> :sswitch_77
        0x58e4f641 -> :sswitch_2d
    .end sparse-switch

    :sswitch_data_158
    .sparse-switch
        -0x42f912e3 -> :sswitch_44
        -0x1db758e4 -> :sswitch_aa
        -0x1c72fb97 -> :sswitch_a5
        0x2d15ec44 -> :sswitch_c7
    .end sparse-switch

    :sswitch_data_16a
    .sparse-switch
        -0x4acb0544 -> :sswitch_b9
        -0x3217c16c -> :sswitch_63
        0x10708af -> :sswitch_bc
        0x54a803b6 -> :sswitch_b0
    .end sparse-switch

    :sswitch_data_17c
    .sparse-switch
        -0x53e2dc90 -> :sswitch_2d
        0xdecf9a4 -> :sswitch_91
        0x74d44c8a -> :sswitch_9f
        0x790aa8da -> :sswitch_96
    .end sparse-switch

    :sswitch_data_18e
    .sparse-switch
        -0x48eedf3c -> :sswitch_101
        -0x1a9124a0 -> :sswitch_117
        0x3ff54152 -> :sswitch_106
        0x7febfcff -> :sswitch_ee
    .end sparse-switch
.end method

.method private static 岬(Ljava/io/InputStream;Ljava/io/InputStream;)Z
    .registers 12

    const/4 v1, 0x0

    :try_start_1
    invoke-virtual {p0}, Ljava/io/InputStream;->available()I

    move-result v3

    invoke-virtual {p1}, Ljava/io/InputStream;->available()I

    move-result v2

    const v4, -0x53fccccf

    const-string v0, "\u06e6\u06e8\u06e5\u06df\u06db\u06e5\u06d8\u06d9\u06d6\u06df\u06d8\u06e5\u06e4\u06e1\u06da\u06e1\u06d8\u06e6\u06dc\u06dc\u06e8\u06e2\u06e1\u06d8\u06d9\u06e7\u06e6"

    :goto_e
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I
    :try_end_11
    .catch Ljava/io/FileNotFoundException; {:try_start_1 .. :try_end_11} :catch_7c
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_11} :catch_84
    .catchall {:try_start_1 .. :try_end_11} :catchall_8c

    move-result v5

    xor-int/2addr v5, v4

    sparse-switch v5, :sswitch_data_94

    goto :goto_e

    :sswitch_17
    const-string v0, "\u06e8\u06d9\u06d8\u06d8\u06e8\u06eb\u06dc\u06e5\u06e8\u06e8\u06d8\u06eb\u06e0\u06e8\u06da\u06e6\u06e8\u06e1\u06e5\u06e5"

    goto :goto_e

    :cond_1a
    :try_start_1a
    const-string v0, "\u06d6\u06ec\u06df\u06d9\u06d7\u06e0\u06e4\u06ec\u06ec\u06e5\u06da\u06e8\u06e2\u06e1\u06d8\u06e4\u06db\u06ec\u06d6\u06d6\u06e5\u06eb\u06dc\u06ec\u06e1\u06e4\u06dc\u06d8"

    goto :goto_e

    :sswitch_1d
    if-eq v3, v2, :cond_1a

    const-string v0, "\u06ec\u06da\u06d9\u06e4\u06d8\u06d7\u06da\u06d6\u06ec\u06d7\u06db\u06e5\u06d8\u06e4\u06eb\u06e1\u06d8\u06db\u06e6\u06e5\u06d6\u06d6\u06df"
    :try_end_21
    .catch Ljava/io/FileNotFoundException; {:try_start_1a .. :try_end_21} :catch_7c
    .catch Ljava/io/IOException; {:try_start_1a .. :try_end_21} :catch_84
    .catchall {:try_start_1a .. :try_end_21} :catchall_8c

    goto :goto_e

    :sswitch_22
    invoke-static {p0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {p1}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    :goto_28
    return v1

    :sswitch_29
    :try_start_29
    new-array v4, v3, [B

    new-array v5, v2, [B

    invoke-virtual {p0, v4}, Ljava/io/InputStream;->read([B)I

    invoke-virtual {p1, v5}, Ljava/io/InputStream;->read([B)I
    :try_end_33
    .catch Ljava/io/FileNotFoundException; {:try_start_29 .. :try_end_33} :catch_7c
    .catch Ljava/io/IOException; {:try_start_29 .. :try_end_33} :catch_84
    .catchall {:try_start_29 .. :try_end_33} :catchall_8c

    move v0, v1

    :goto_34
    const v6, 0x11bb0785

    const-string v2, "\u06d7\u06d6\u06e8\u06d8\u06df\u06e6\u06e5\u06d8\u06df\u06e1\u06dc\u06df\u06e4\u06e8\u06d8\u06df\u06e2\u06dc\u06d8\u06e5\u06eb\u06d8"

    :goto_39
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v7

    xor-int/2addr v7, v6

    sparse-switch v7, :sswitch_data_a6

    goto :goto_39

    :sswitch_42
    invoke-static {p0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {p1}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    const/4 v1, 0x1

    goto :goto_28

    :cond_4a
    const-string v2, "\u06e0\u06e7\u06e5\u06d8\u06d6\u06e6\u06e1\u06e2\u06d6\u06ec\u06dc\u06e0\u06e5\u06eb\u06e5\u06e0\u06e2\u06da"

    goto :goto_39

    :sswitch_4d
    if-ge v0, v3, :cond_4a

    const-string v2, "\u06d7\u06ec\u06e1\u06d8\u06d7\u06e8\u06df\u06e1\u06ec\u06e6\u06df\u06ec\u06da\u06e5\u06e4\u06e2\u06e2\u06e1\u06d7\u06d9\u06e7\u06dc\u06d6\u06e8\u06e7"

    goto :goto_39

    :sswitch_52
    const-string v2, "\u06dc\u06e8\u06e1\u06d8\u06eb\u06e1\u06e1\u06df\u06eb\u06e1\u06db\u06e5\u06e6\u06d8\u06e0\u06d7\u06e6\u06d8"

    goto :goto_39

    :sswitch_55
    aget-byte v6, v4, v0

    aget-byte v7, v5, v0

    const v8, -0x203f0a76

    const-string v2, "\u06d7\u06e8\u06d9\u06e2\u06e4\u06e8\u06eb\u06e0\u06e1\u06d8\u06e7\u06db\u06e8\u06d8\u06eb\u06e6\u06eb\u06d7\u06e2\u06d8\u06d8"

    :goto_5e
    invoke-virtual {v2}, Ljava/lang/String;->hashCode()I

    move-result v9

    xor-int/2addr v9, v8

    sparse-switch v9, :sswitch_data_b8

    goto :goto_5e

    :sswitch_67
    add-int/lit8 v0, v0, 0x1

    goto :goto_34

    :cond_6a
    const-string v2, "\u06d6\u06dc\u06e7\u06eb\u06eb\u06d6\u06d8\u06e5\u06e4\u06e0\u06d9\u06d6\u06d8\u06e8\u06d7\u06dc\u06eb\u06e8\u06dc\u06db\u06d6\u06e7"

    goto :goto_5e

    :sswitch_6d
    if-eq v6, v7, :cond_6a

    const-string v2, "\u06df\u06d8\u06d6\u06d8\u06eb\u06da\u06dc\u06d8\u06d9\u06d6\u06db\u06d9\u06eb\u06e4\u06e7\u06e7\u06db\u06e1\u06d6\u06e8\u06e7\u06e2\u06e8\u06d8\u06e1\u06d9\u06e8"

    goto :goto_5e

    :sswitch_72
    const-string v2, "\u06da\u06e5\u06e2\u06dc\u06db\u06e1\u06eb\u06e8\u06d8\u06e0\u06e1\u06e4\u06d6\u06d7\u06dc\u06e7\u06da\u06d8\u06d8\u06e7\u06dc\u06e6\u06d8"

    goto :goto_5e

    :sswitch_75
    invoke-static {p0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {p1}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    goto :goto_28

    :catch_7c
    move-exception v0

    invoke-static {p0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {p1}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    goto :goto_28

    :catch_84
    move-exception v0

    invoke-static {p0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {p1}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    goto :goto_28

    :catchall_8c
    move-exception v0

    invoke-static {p0}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    invoke-static {p1}, Lv/m/岬;->岬(Ljava/io/Closeable;)V

    throw v0

    :sswitch_data_94
    .sparse-switch
        -0x4cb3c3f4 -> :sswitch_22
        0x3828a1c9 -> :sswitch_1d
        0x53416843 -> :sswitch_17
        0x5bb825c8 -> :sswitch_29
    .end sparse-switch

    :sswitch_data_a6
    .sparse-switch
        -0x68bbdfcb -> :sswitch_52
        0x11449d48 -> :sswitch_4d
        0x1d32bb9b -> :sswitch_42
        0x21481bb7 -> :sswitch_55
    .end sparse-switch

    :sswitch_data_b8
    .sparse-switch
        -0x3efb38f8 -> :sswitch_75
        -0x3133b1f9 -> :sswitch_6d
        -0x784c649 -> :sswitch_67
        0x97a22d9 -> :sswitch_72
    .end sparse-switch
.end method

.method public static 惂()V
    .registers 4

    const v1, 0xb6b4411

    const-string v0, "\u06e8\u06e7\u06dc\u06d8\u06eb\u06eb\u06dc\u06d8\u06e2\u06e2\u06e6\u06d8\u06d7\u06e5\u06eb\u06e8\u06dc\u06e2"

    :goto_5
    invoke-virtual {v0}, Ljava/lang/String;->hashCode()I

    move-result v2

    xor-int/2addr v2, v1

    sparse-switch v2, :sswitch_data_72

    goto :goto_5

    :sswitch_e
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1c

    if-eq v0, v2, :cond_17

    const-string v0, "\u06e6\u06e6\u06e2\u06e5\u06e4\u06e6\u06d8\u06e4\u06d7\u06d8\u06ec\u06e7\u06e6\u06d8\u06d8\u06e2\u06e4\u06e0\u06e7\u06e2\u06d7\u06dc"

    goto :goto_5

    :cond_17
    const-string v0, "\u06db\u06e4\u06e6\u06d8\u06e1\u06e6\u06d6\u06eb\u06e6\u06db\u06ec\u06d6\u06d8\u06eb\u06e5\u06d7\u06e7\u06eb\u06da\u06d6\u06e4\u06d7\u06e6\u06d7\u06e0\u06e6\u06ec\u06e8"

    goto :goto_5

    :sswitch_1a
    const-string v0, "\u06d6\u06d6\u06e0\u06e0\u06ec\u06d9\u06e8\u06e8\u06e6\u06e2\u06e0\u06e4\u06df\u06e8\u06e5\u06d8"

    goto :goto_5

    :sswitch_1d
    :try_start_1d
    const-string v0, "q~tb\u007fyt>s\u007f~du~d>`}>@qs{qwu@qbcub4@qs{qwu"

    invoke-static {v0}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    const/4 v2, 0x0

    const-class v3, Ljava/lang/String;

    aput-object v3, v1, v2

    invoke-virtual {v0, v1}, Ljava/lang/Class;->getDeclaredConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v0

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/lang/reflect/Constructor;->setAccessible(Z)V
    :try_end_37
    .catch Ljava/lang/Throwable; {:try_start_1d .. :try_end_37} :catch_6d

    :goto_37
    :try_start_37
    const-string v0, "q~tb\u007fyt>q``>QsdyfydiDxbuqt"

    invoke-static {v0}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    const-string v1, "sebbu~dQsdyfydiDxbuqt"

    invoke-static {v1}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    new-array v2, v2, [Ljava/lang/Class;

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    const/4 v2, 0x1

    invoke-virtual {v1, v2}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    const/4 v2, 0x0

    const/4 v3, 0x0

    new-array v3, v3, [Ljava/lang/Object;

    invoke-virtual {v1, v2, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    const-string v2, "}Xyttu~Q`yGqb~y~wCx\u007fg~"

    invoke-static {v2}, Lv/m/岬;->岬(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v0, v2}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    const/4 v2, 0x1

    invoke-virtual {v0, v2}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    const/4 v2, 0x1

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Field;->setBoolean(Ljava/lang/Object;Z)V
    :try_end_6c
    .catch Ljava/lang/Throwable; {:try_start_37 .. :try_end_6c} :catch_6f

    :goto_6c
    :sswitch_6c
    return-void

    :catch_6d
    move-exception v0

    goto :goto_37

    :catch_6f
    move-exception v0

    goto :goto_6c

    nop

    :sswitch_data_72
    .sparse-switch
        -0x655fc308 -> :sswitch_6c
        0x4b338bb4 -> :sswitch_1a
        0x7811804b -> :sswitch_e
        0x7f3bed4e -> :sswitch_1d
    .end sparse-switch
.end method
