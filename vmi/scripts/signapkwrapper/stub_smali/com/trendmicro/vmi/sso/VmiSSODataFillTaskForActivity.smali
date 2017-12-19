.class public Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;
.super Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;
.source "VmiSSODataFillTaskForActivity.java"


# instance fields
.field private activityTarget:Landroid/app/Activity;


# direct methods
.method public constructor <init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;Landroid/app/Activity;ILjava/lang/String;)V
    .registers 6
    .param p1, "vsh"    # Lcom/trendmicro/vmi/sso/VmiSSOHelper;
    .param p2, "activityTarget"    # Landroid/app/Activity;
    .param p3, "tvControlId"    # I
    .param p4, "infoKey"    # Ljava/lang/String;

    .prologue
    .line 19
    invoke-direct {p0, p1, p3, p4}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;-><init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;ILjava/lang/String;)V

    .line 15
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->activityTarget:Landroid/app/Activity;

    .line 21
    iput-object p2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->activityTarget:Landroid/app/Activity;

    .line 22
    return-void
.end method


# virtual methods
.method protected getTextView(I)Landroid/widget/TextView;
    .registers 3
    .param p1, "tvControlId"    # I

    .prologue
    .line 31
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->activityTarget:Landroid/app/Activity;

    invoke-virtual {v0, p1}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/TextView;

    return-object v0
.end method

.method protected postToUiInternal(ILjava/lang/String;Ljava/lang/String;)V
    .registers 8
    .param p1, "tvControlId"    # I
    .param p2, "infoKey"    # Ljava/lang/String;
    .param p3, "infoValue"    # Ljava/lang/String;

    .prologue
    .line 36
    move-object v0, p0

    .line 37
    .local v0, "thisTask":Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;
    invoke-virtual {p0, p1}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->getTextView(I)Landroid/widget/TextView;

    move-result-object v1

    .line 39
    .local v1, "tvTarget":Landroid/widget/TextView;
    if-eqz v1, :cond_11

    .line 40
    iget-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->activityTarget:Landroid/app/Activity;

    new-instance v3, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;

    invoke-direct {v3, p0, v1, p3, v0}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;-><init>(Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;Landroid/widget/TextView;Ljava/lang/String;Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;)V

    invoke-virtual {v2, v3}, Landroid/app/Activity;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 52
    :cond_11
    iget-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    invoke-virtual {v2}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->dismissProgressDialog()V

    .line 53
    return-void
.end method
