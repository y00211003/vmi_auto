.class public Lcom/trendmicro/vmi/sso/VmiSSOData;
.super Ljava/lang/Object;
.source "VmiSSOData.java"


# static fields
.field public static KEY_EXCHANGE_SERVER:Ljava/lang/String;

.field public static KEY_OTHER_SERVER:Ljava/lang/String;

.field public static KEY_OTHER_SERVER_PORT:Ljava/lang/String;

.field public static KEY_PASSWORD:Ljava/lang/String;

.field public static KEY_USERNAME:Ljava/lang/String;

.field public static KEY_USERNAME_EMAIL:Ljava/lang/String;

.field public static KEY_USERNAME_WITHOUT_DOMAIN:Ljava/lang/String;

.field public static STUB_ALWAYS_WITHOUT_DOMAIN:Ljava/lang/String;

.field public static STUB_OTHER_SERVER:Ljava/lang/String;

.field public static STUB_OTHER_SERVER_PORT:Ljava/lang/String;

.field public static STUB_WAIT_TIME:Ljava/lang/String;

.field private static initialized:Z

.field private static isDomainAccount:Z

.field private static isUserNameFilled:Z

.field private static mapValue:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private static setKeyBlockedByUsername:Ljava/util/Set;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Set",
            "<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .registers 2

    .prologue
    const/4 v1, 0x0

    .line 16
    const-string v0, "username"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME:Ljava/lang/String;

    .line 17
    const-string v0, "usernameWithoutDomain"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME_WITHOUT_DOMAIN:Ljava/lang/String;

    .line 18
    const-string v0, "usernameEmail"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME_EMAIL:Ljava/lang/String;

    .line 19
    const-string v0, "password"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_PASSWORD:Ljava/lang/String;

    .line 20
    const-string v0, "exchangeServer"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_EXCHANGE_SERVER:Ljava/lang/String;

    .line 21
    const-string v0, "otherServer"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_OTHER_SERVER:Ljava/lang/String;

    .line 22
    const-string v0, "otherServerPort"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_OTHER_SERVER_PORT:Ljava/lang/String;

    .line 24
    const-string v0, "$ALWAYS_WITHOUT_DOMAIN$"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_ALWAYS_WITHOUT_DOMAIN:Ljava/lang/String;

    .line 25
    const-string v0, "$WAIT_TIME$"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_WAIT_TIME:Ljava/lang/String;

    .line 26
    const-string v0, "$OTHER_SERVER$"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_OTHER_SERVER:Ljava/lang/String;

    .line 27
    const-string v0, "$OTHER_SERVER_PORT$"

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_OTHER_SERVER_PORT:Ljava/lang/String;

    .line 29
    sput-boolean v1, Lcom/trendmicro/vmi/sso/VmiSSOData;->initialized:Z

    .line 30
    new-instance v0, Ljava/util/HashMap;

    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->mapValue:Ljava/util/Map;

    .line 31
    sput-boolean v1, Lcom/trendmicro/vmi/sso/VmiSSOData;->isDomainAccount:Z

    .line 33
    new-instance v0, Ljava/util/HashSet;

    invoke-direct {v0}, Ljava/util/HashSet;-><init>()V

    sput-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->setKeyBlockedByUsername:Ljava/util/Set;

    .line 34
    sput-boolean v1, Lcom/trendmicro/vmi/sso/VmiSSOData;->isUserNameFilled:Z

    .line 37
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->setKeyBlockedByUsername:Ljava/util/Set;

    sget-object v1, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_PASSWORD:Ljava/lang/String;

    invoke-interface {v0, v1}, Ljava/util/Set;->add(Ljava/lang/Object;)Z

    .line 38
    return-void
.end method

.method public constructor <init>()V
    .registers 1

    .prologue
    .line 14
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static getMapValue(Ljava/lang/String;)Ljava/lang/String;
    .registers 2
    .param p0, "key"    # Ljava/lang/String;

    .prologue
    .line 59
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->mapValue:Ljava/util/Map;

    invoke-interface {v0, p0}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    return-object v0
.end method

.method public static isBlockedByUserName(Ljava/lang/String;)Z
    .registers 2
    .param p0, "key"    # Ljava/lang/String;

    .prologue
    .line 75
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->setKeyBlockedByUsername:Ljava/util/Set;

    invoke-interface {v0, p0}, Ljava/util/Set;->contains(Ljava/lang/Object;)Z

    move-result v0

    return v0
.end method

.method public static isDomainAccount()Z
    .registers 1

    .prologue
    .line 63
    sget-boolean v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->isDomainAccount:Z

    return v0
.end method

.method public static isInitialized()Z
    .registers 1

    .prologue
    .line 41
    sget-boolean v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->initialized:Z

    return v0
.end method

.method public static isUserNameFilled()Z
    .registers 1

    .prologue
    .line 71
    sget-boolean v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->isUserNameFilled:Z

    return v0
.end method

.method public static setInitialized(Z)V
    .registers 1
    .param p0, "initialized"    # Z

    .prologue
    .line 45
    sput-boolean p0, Lcom/trendmicro/vmi/sso/VmiSSOData;->initialized:Z

    .line 46
    return-void
.end method

.method public static setMapValue(Ljava/lang/String;Ljava/lang/String;)V
    .registers 3
    .param p0, "key"    # Ljava/lang/String;
    .param p1, "value"    # Ljava/lang/String;

    .prologue
    .line 49
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->mapValue:Ljava/util/Map;

    invoke-interface {v0, p0, p1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 51
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME:Ljava/lang/String;

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_18

    .line 52
    const-string v0, "\\"

    invoke-virtual {p1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-eqz v0, :cond_18

    .line 53
    const/4 v0, 0x1

    sput-boolean v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->isDomainAccount:Z

    .line 56
    :cond_18
    return-void
.end method

.method public static setUserNameFilled()V
    .registers 1

    .prologue
    .line 67
    const/4 v0, 0x1

    sput-boolean v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->isUserNameFilled:Z

    .line 68
    return-void
.end method
