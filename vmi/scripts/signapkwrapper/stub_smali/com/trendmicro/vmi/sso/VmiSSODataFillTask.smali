.class public abstract Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;
.super Ljava/lang/Object;
.source "VmiSSODataFillTask.java"


# static fields
.field private static final PERIOD_MS:I = 0x1f4

.field private static final WAIT_MS:I = 0x1f4


# instance fields
.field protected blocked:Z

.field protected infoKey:Ljava/lang/String;

.field protected postedToUI:Z

.field protected taskTimer:Ljava/util/Timer;

.field protected tvControlId:I

.field protected vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;


# direct methods
.method public constructor <init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;ILjava/lang/String;)V
    .registers 7
    .param p1, "vsh"    # Lcom/trendmicro/vmi/sso/VmiSSOHelper;
    .param p2, "tvControlId"    # I
    .param p3, "infoKey"    # Ljava/lang/String;

    .prologue
    const/4 v2, 0x0

    const/4 v1, 0x0

    .line 27
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 20
    iput-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    .line 21
    iput v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->tvControlId:I

    .line 22
    const-string v0, ""

    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->infoKey:Ljava/lang/String;

    .line 23
    iput-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->taskTimer:Ljava/util/Timer;

    .line 24
    iput-boolean v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->postedToUI:Z

    .line 25
    iput-boolean v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->blocked:Z

    .line 28
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    .line 29
    iput p2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->tvControlId:I

    .line 30
    iput-object p3, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->infoKey:Ljava/lang/String;

    .line 31
    return-void
.end method

.method protected static filledInfo(Ljava/lang/String;)V
    .registers 2
    .param p0, "infoKey"    # Ljava/lang/String;

    .prologue
    .line 83
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME:Ljava/lang/String;

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_18

    .line 84
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME_WITHOUT_DOMAIN:Ljava/lang/String;

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_18

    .line 85
    sget-object v0, Lcom/trendmicro/vmi/sso/VmiSSOData;->KEY_USERNAME_EMAIL:Ljava/lang/String;

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1b

    .line 86
    :cond_18
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->setUserNameFilled()V

    .line 88
    :cond_1b
    return-void
.end method

.method protected static isUserNameFilled()Z
    .registers 1

    .prologue
    .line 97
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isUserNameFilled()Z

    move-result v0

    return v0
.end method

.method protected static needWaitOtherInfo(Ljava/lang/String;)Z
    .registers 2
    .param p0, "infoKey"    # Ljava/lang/String;

    .prologue
    .line 109
    invoke-static {p0}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isBlockedByUserName(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_e

    .line 110
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isUserNameFilled()Z

    move-result v0

    if-nez v0, :cond_e

    .line 112
    const/4 v0, 0x1

    .line 116
    :goto_d
    return v0

    :cond_e
    const/4 v0, 0x0

    goto :goto_d
.end method


# virtual methods
.method public arrageDataFillTask()V
    .registers 8

    .prologue
    const-wide/16 v2, 0x1f4

    .line 123
    new-instance v0, Ljava/util/Timer;

    invoke-direct {v0}, Ljava/util/Timer;-><init>()V

    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->taskTimer:Ljava/util/Timer;

    .line 124
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->infoKey:Ljava/lang/String;

    invoke-static {v0}, Lcom/trendmicro/vmi/sso/VmiSSOData;->getMapValue(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    .line 125
    .local v6, "infoValue":Ljava/lang/String;
    if-nez v6, :cond_12

    .line 152
    :goto_11
    return-void

    .line 128
    :cond_12
    new-instance v1, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;

    invoke-direct {v1, p0, v6}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;-><init>(Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;Ljava/lang/String;)V

    .line 151
    .local v1, "task":Ljava/util/TimerTask;
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->taskTimer:Ljava/util/Timer;

    move-wide v4, v2

    invoke-virtual/range {v0 .. v5}, Ljava/util/Timer;->scheduleAtFixedRate(Ljava/util/TimerTask;JJ)V

    goto :goto_11
.end method

.method protected abstract getTextView(I)Landroid/widget/TextView;
.end method

.method protected postToUi(ILjava/lang/String;Ljava/lang/String;)V
    .registers 6
    .param p1, "tvControlId"    # I
    .param p2, "infoKey"    # Ljava/lang/String;
    .param p3, "infoValue"    # Ljava/lang/String;

    .prologue
    .line 60
    invoke-virtual {p0, p1}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->getTextView(I)Landroid/widget/TextView;

    move-result-object v0

    .line 62
    .local v0, "tvTarget":Landroid/widget/TextView;
    iget-boolean v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->postedToUI:Z

    if-eqz v1, :cond_25

    .line 63
    if-eqz v0, :cond_21

    .line 64
    invoke-virtual {v0}, Landroid/widget/TextView;->getText()Ljava/lang/CharSequence;

    move-result-object v1

    invoke-interface {v1}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1, p3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_21

    .line 65
    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->taskTimer:Ljava/util/Timer;

    invoke-virtual {v1}, Ljava/util/Timer;->cancel()V

    .line 66
    invoke-static {p2}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->filledInfo(Ljava/lang/String;)V

    .line 75
    :goto_20
    return-void

    .line 68
    :cond_21
    const/4 v1, 0x0

    iput-boolean v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->postedToUI:Z

    goto :goto_20

    .line 74
    :cond_25
    invoke-virtual {p0, p1, p2, p3}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->postToUiInternal(ILjava/lang/String;Ljava/lang/String;)V

    goto :goto_20
.end method

.method protected abstract postToUiInternal(ILjava/lang/String;Ljava/lang/String;)V
.end method
