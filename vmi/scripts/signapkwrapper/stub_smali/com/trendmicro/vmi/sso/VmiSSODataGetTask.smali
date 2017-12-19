.class public Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;
.super Landroid/os/AsyncTask;
.source "VmiSSODataGetTask.java"


# annotations
.annotation system Ldalvik/annotation/Signature;
    value = {
        "Landroid/os/AsyncTask",
        "<",
        "Ljava/lang/Void;",
        "Ljava/lang/Void;",
        "Lcom/trendmicro/vmi/sso/TaskResult;",
        ">;"
    }
.end annotation


# instance fields
.field private vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;


# direct methods
.method public constructor <init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;)V
    .registers 3
    .param p1, "vsh"    # Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    .prologue
    .line 24
    invoke-direct {p0}, Landroid/os/AsyncTask;-><init>()V

    .line 22
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    .line 25
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    .line 26
    return-void
.end method


# virtual methods
.method protected varargs doInBackground([Ljava/lang/Void;)Lcom/trendmicro/vmi/sso/TaskResult;
    .registers 7
    .param p1, "v"    # [Ljava/lang/Void;

    .prologue
    .line 30
    new-instance v2, Lcom/trendmicro/vmi/sso/TaskResult;

    invoke-direct {v2}, Lcom/trendmicro/vmi/sso/TaskResult;-><init>()V

    .line 31
    .local v2, "result":Lcom/trendmicro/vmi/sso/TaskResult;
    const/4 v3, 0x0

    iput-boolean v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->got:Z

    .line 32
    const-string v3, ""

    iput-object v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->vmiAuthComb:Ljava/lang/String;

    .line 33
    const-string v3, ""

    iput-object v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->vmiExchangeServer:Ljava/lang/String;

    .line 34
    const-string v3, ""

    iput-object v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->vmiExchangeSuffix:Ljava/lang/String;

    .line 37
    :try_start_14
    new-instance v0, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;

    invoke-direct {v0}, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;-><init>()V

    .line 38
    .local v0, "auth":Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;
    invoke-virtual {v0}, Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;->getAuthToken()Ljava/lang/String;

    move-result-object v3

    iput-object v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->vmiAuthComb:Ljava/lang/String;

    .line 40
    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    .line 41
    invoke-virtual {v3}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->getContext()Landroid/content/Context;

    move-result-object v3

    invoke-virtual {v3}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v3

    const-string v4, "eas.exchangeServer"

    .line 40
    invoke-static {v3, v4}, Landroid/provider/Settings$Secure;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    iput-object v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->vmiExchangeServer:Ljava/lang/String;

    .line 42
    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    .line 43
    invoke-virtual {v3}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->getContext()Landroid/content/Context;

    move-result-object v3

    invoke-virtual {v3}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v3

    const-string v4, "eas.exchangeSuffix"

    .line 42
    invoke-static {v3, v4}, Landroid/provider/Settings$Secure;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    iput-object v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->vmiExchangeSuffix:Ljava/lang/String;

    .line 45
    const/4 v3, 0x1

    iput-boolean v3, v2, Lcom/trendmicro/vmi/sso/TaskResult;->got:Z
    :try_end_46
    .catch Ljava/lang/Exception; {:try_start_14 .. :try_end_46} :catch_47

    .line 53
    .end local v0    # "auth":Lcom/trendmicro/vmi/sso/VmiQemudAuthenticator;
    :goto_46
    return-object v2

    .line 48
    :catch_47
    move-exception v1

    .line 49
    .local v1, "ex":Ljava/lang/Exception;
    const-string v3, "VMIWrapper"

    const-string v4, "Get VMI SSO data failed!"

    invoke-static {v3, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 50
    invoke-virtual {v1}, Ljava/lang/Exception;->printStackTrace()V

    goto :goto_46
.end method

.method protected bridge varargs synthetic doInBackground([Ljava/lang/Object;)Ljava/lang/Object;
    .registers 3

    .prologue
    .line 1
    check-cast p1, [Ljava/lang/Void;

    invoke-virtual {p0, p1}, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->doInBackground([Ljava/lang/Void;)Lcom/trendmicro/vmi/sso/TaskResult;

    move-result-object v0

    return-object v0
.end method

.method protected onPostExecute(Lcom/trendmicro/vmi/sso/TaskResult;)V
    .registers 11
    .param p1, "result"    # Lcom/trendmicro/vmi/sso/TaskResult;

    .prologue
    const/4 v8, 0x2

    const/4 v6, 0x0

    const/4 v7, 0x1

    .line 58
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isInitialized()Z

    move-result v4

    if-nez v4, :cond_80

    .line 59
    iget-boolean v4, p1, Lcom/trendmicro/vmi/sso/TaskResult;->got:Z

    if-eqz v4, :cond_91

    .line 60
    iget-object v4, p1, Lcom/trendmicro/vmi/sso/TaskResult;->vmiAuthComb:Ljava/lang/String;

    const-string v5, "\\|"

    invoke-virtual {v4, v5, v8}, Ljava/lang/String;->split(Ljava/lang/String;I)[Ljava/lang/String;

    move-result-object v0

    .line 61
    .local v0, "namePswd":[Ljava/lang/String;
    aget-object v2, v0, v6

    .line 62
    .local v2, "username":Ljava/lang/String;
    aget-object v1, v0, v7

    .line 64
    .local v1, "password":Ljava/lang/String;
    const-string v3, ""

    .line 65
    .local v3, "usernameWithoutDomain":Ljava/lang/String;
    const-string v4, "\\"

    invoke-virtual {v2, v4}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v4

    if-eqz v4, :cond_89

    .line 66
    const-string v4, "\\\\"

    invoke-virtual {v2, v4, v8}, Ljava/lang/String;->split(Ljava/lang/String;I)[Ljava/lang/String;

    move-result-object v4

    aget-object v3, v4, v7

    .line 71
    :goto_2b
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_ALWAYS_WITHOUT_DOMAIN:Ljava/lang/String;

    .line 72
    const-string v5, "true"

    invoke-virtual {v4, v5}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v4

    if-eqz v4, :cond_8b

    .line 73
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME:Ljava/lang/String;

    invoke-static {v4, v3}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    .line 78
    :goto_3a
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME_WITHOUT_DOMAIN:Ljava/lang/String;

    invoke-static {v4, v3}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    .line 80
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_PASSWORD:Ljava/lang/String;

    invoke-static {v4, v1}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    .line 81
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_EXCHANGE_SERVER:Ljava/lang/String;

    .line 82
    iget-object v5, p1, Lcom/trendmicro/vmi/sso/TaskResult;->vmiExchangeServer:Ljava/lang/String;

    .line 81
    invoke-static {v4, v5}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    .line 83
    iget-object v4, p1, Lcom/trendmicro/vmi/sso/TaskResult;->vmiExchangeSuffix:Ljava/lang/String;

    const-string v5, ""

    if-eq v4, v5, :cond_6f

    .line 84
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME_EMAIL:Ljava/lang/String;

    .line 85
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-static {v3}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v6

    invoke-direct {v5, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v6, "@"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    .line 86
    iget-object v6, p1, Lcom/trendmicro/vmi/sso/TaskResult;->vmiExchangeSuffix:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    .line 85
    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    .line 84
    invoke-static {v4, v5}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    .line 89
    :cond_6f
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_OTHER_SERVER:Ljava/lang/String;

    .line 90
    sget-object v5, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_OTHER_SERVER:Ljava/lang/String;

    .line 89
    invoke-static {v4, v5}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    .line 91
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_OTHER_SERVER_PORT:Ljava/lang/String;

    .line 92
    sget-object v5, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_OTHER_SERVER_PORT:Ljava/lang/String;

    .line 91
    invoke-static {v4, v5}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    .line 94
    invoke-static {v7}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setInitialized(Z)V

    .line 101
    .end local v0    # "namePswd":[Ljava/lang/String;
    .end local v1    # "password":Ljava/lang/String;
    .end local v2    # "username":Ljava/lang/String;
    .end local v3    # "usernameWithoutDomain":Ljava/lang/String;
    :cond_80
    :goto_80
    iget-object v4, p0, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    invoke-virtual {v4}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->setSSOInfo()V

    .line 103
    invoke-super {p0, p1}, Landroid/os/AsyncTask;->onPostExecute(Ljava/lang/Object;)V

    .line 104
    return-void

    .line 68
    .restart local v0    # "namePswd":[Ljava/lang/String;
    .restart local v1    # "password":Ljava/lang/String;
    .restart local v2    # "username":Ljava/lang/String;
    .restart local v3    # "usernameWithoutDomain":Ljava/lang/String;
    :cond_89
    move-object v3, v2

    goto :goto_2b

    .line 76
    :cond_8b
    sget-object v4, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME:Ljava/lang/String;

    invoke-static {v4, v2}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setMapValue(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_3a

    .line 96
    .end local v0    # "namePswd":[Ljava/lang/String;
    .end local v1    # "password":Ljava/lang/String;
    .end local v2    # "username":Ljava/lang/String;
    .end local v3    # "usernameWithoutDomain":Ljava/lang/String;
    :cond_91
    invoke-static {v6}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setInitialized(Z)V

    goto :goto_80
.end method

.method protected bridge synthetic onPostExecute(Ljava/lang/Object;)V
    .registers 2

    .prologue
    .line 1
    check-cast p1, Lcom/trendmicro/vmi/sso/TaskResult;

    invoke-virtual {p0, p1}, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->onPostExecute(Lcom/trendmicro/vmi/sso/TaskResult;)V

    return-void
.end method
