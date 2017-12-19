.class public Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;
.super Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;
.source "VmiSSODataFillTaskForView.java"


# instance fields
.field private viewTarget:Landroid/view/View;


# direct methods
.method public constructor <init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;Landroid/view/View;ILjava/lang/String;)V
    .registers 6
    .param p1, "vsh"    # Lcom/trendmicro/vmi/sso/VmiSSOHelper;
    .param p2, "viewTarget"    # Landroid/view/View;
    .param p3, "tvControlId"    # I
    .param p4, "infoKey"    # Ljava/lang/String;

    .prologue
    .line 19
    invoke-direct {p0, p1, p3, p4}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;-><init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;ILjava/lang/String;)V

    .line 15
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->viewTarget:Landroid/view/View;

    .line 21
    iput-object p2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->viewTarget:Landroid/view/View;

    .line 22
    return-void
.end method


# virtual methods
.method protected getTextView(I)Landroid/widget/TextView;
    .registers 3
    .param p1, "tvControlId"    # I

    .prologue
    .line 31
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->viewTarget:Landroid/view/View;

    invoke-virtual {v0, p1}, Landroid/view/View;->findViewById(I)Landroid/view/View;

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
    invoke-virtual {p0, p1}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->getTextView(I)Landroid/widget/TextView;

    move-result-object v1

    .line 39
    .local v1, "tvTarget":Landroid/widget/TextView;
    iget-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->viewTarget:Landroid/view/View;

    invoke-virtual {v2}, Landroid/view/View;->isShown()Z

    move-result v2

    if-eqz v2, :cond_19

    if-eqz v1, :cond_19

    .line 40
    iget-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->viewTarget:Landroid/view/View;

    new-instance v3, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView$1;

    invoke-direct {v3, p0, v1, p3, v0}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView$1;-><init>(Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;Landroid/widget/TextView;Ljava/lang/String;Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;)V

    invoke-virtual {v2, v3}, Landroid/view/View;->post(Ljava/lang/Runnable;)Z

    .line 53
    :cond_19
    iget-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->vsh:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    invoke-virtual {v2}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->dismissProgressDialog()V

    .line 54
    return-void
.end method
