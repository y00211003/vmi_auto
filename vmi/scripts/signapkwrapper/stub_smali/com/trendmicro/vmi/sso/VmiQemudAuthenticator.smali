.class public Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;
.super Ljava/lang/Object;
.source "VmiQemudAuthenticator.java"


# static fields
.field private static final QEMUD_REQUEST_CRED:Ljava/lang/String; = "get:credentials"

.field private static final QEMUD_REQUEST_KEY:Ljava/lang/String; = "get:key"


# instance fields
.field protected qemud:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;


# direct methods
.method public constructor <init>()V
    .registers 2

    .prologue
    .line 18
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 23
    invoke-static {}, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->getInstance()Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    move-result-object v0

    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->qemud:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    .line 18
    return-void
.end method

.method private getPlainPassword(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .registers 9
    .param p1, "storedPassword"    # Ljava/lang/String;
    .param p2, "keyString"    # Ljava/lang/String;

    .prologue
    .line 52
    :try_start_0
    new-instance v3, Ljavax/crypto/spec/SecretKeySpec;

    invoke-virtual {p2}, Ljava/lang/String;->getBytes()[B

    move-result-object v4

    .line 53
    const-string v5, "Blowfish"

    .line 52
    invoke-direct {v3, v4, v5}, Ljavax/crypto/spec/SecretKeySpec;-><init>([BLjava/lang/String;)V

    .line 54
    .local v3, "key":Ljavax/crypto/spec/SecretKeySpec;
    const-string v4, "Blowfish"

    invoke-static {v4}, Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v0

    .line 55
    .local v0, "cipher":Ljavax/crypto/Cipher;
    const/4 v4, 0x2

    invoke-virtual {v0, v4, v3}, Ljavax/crypto/Cipher;->init(ILjava/security/Key;)V

    .line 57
    const/4 v4, 0x0

    .line 56
    invoke-static {p1, v4}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B

    move-result-object v1

    .line 58
    .local v1, "cipherByteArray":[B
    new-instance v4, Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljavax/crypto/Cipher;->doFinal([B)[B

    move-result-object v5

    invoke-direct {v4, v5}, Ljava/lang/String;-><init>([B)V
    :try_end_23
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_23} :catch_24

    .line 60
    .end local v0    # "cipher":Ljavax/crypto/Cipher;
    .end local v1    # "cipherByteArray":[B
    .end local v3    # "key":Ljavax/crypto/spec/SecretKeySpec;
    :goto_23
    return-object v4

    .line 59
    :catch_24
    move-exception v2

    .line 60
    .local v2, "e":Ljava/lang/Exception;
    const/4 v4, 0x0

    goto :goto_23
.end method

.method private getQemudResponse(Ljava/lang/String;)Ljava/lang/String;
    .registers 8
    .param p1, "request"    # Ljava/lang/String;

    .prologue
    const/4 v2, 0x0

    .line 26
    const-string v1, "sso"

    .line 27
    .local v1, "qemudServiceName":Ljava/lang/String;
    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->qemud:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    invoke-virtual {v3, v1}, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->qemudOpen(Ljava/lang/String;)I

    move-result v0

    .line 28
    .local v0, "channel":I
    if-gez v0, :cond_20

    .line 29
    const-string v3, "VMIWrapper"

    new-instance v4, Ljava/lang/StringBuilder;

    const-string v5, "Failed to open qemud service "

    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 30
    invoke-virtual {v4, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    .line 29
    invoke-static {v3, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 47
    :goto_1f
    return-object v2

    .line 34
    :cond_20
    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->qemud:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    const/4 v4, -0x1

    invoke-virtual {v3, v0, p1, v4}, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->qemudSend(ILjava/lang/String;I)I

    move-result v3

    if-eqz v3, :cond_43

    .line 35
    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->qemud:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    invoke-virtual {v3, v0}, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->qemudClose(I)V

    .line 36
    const-string v3, "VMIWrapper"

    new-instance v4, Ljava/lang/StringBuilder;

    const-string v5, "Failed to send qemud request "

    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 37
    invoke-virtual {v4, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    .line 36
    invoke-static {v3, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_1f

    .line 43
    :cond_43
    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->qemud:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    invoke-virtual {v3, v0}, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->qemudReceive(I)Ljava/lang/String;

    move-result-object v2

    .line 46
    .local v2, "response":Ljava/lang/String;
    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->qemud:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    invoke-virtual {v3, v0}, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->qemudClose(I)V

    goto :goto_1f
.end method


# virtual methods
.method public getAuthToken()Ljava/lang/String;
    .registers 4

    .prologue
    .line 66
    const-string v2, "get:credentials"

    invoke-direct {p0, v2}, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->getQemudResponse(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 67
    .local v0, "credential":Ljava/lang/String;
    const-string v2, "get:key"

    invoke-direct {p0, v2}, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->getQemudResponse(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 69
    .local v1, "key":Ljava/lang/String;
    invoke-direct {p0, v0, v1}, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->getPlainPassword(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 71
    return-object v0
.end method
