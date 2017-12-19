.class Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;
.super Ljava/lang/Object;
.source "VmiSSODataFillTaskForActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->postToUiInternal(ILjava/lang/String;Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;

.field private final synthetic val$infoValue:Ljava/lang/String;

.field private final synthetic val$thisTask:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

.field private final synthetic val$tvTarget:Landroid/widget/TextView;


# direct methods
.method constructor <init>(Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;Landroid/widget/TextView;Ljava/lang/String;Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;)V
    .registers 5

    .prologue
    .line 1
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;

    iput-object p2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;->val$tvTarget:Landroid/widget/TextView;

    iput-object p3, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;->val$infoValue:Ljava/lang/String;

    iput-object p4, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;->val$thisTask:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    .line 40
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 3

    .prologue
    .line 43
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;->val$tvTarget:Landroid/widget/TextView;

    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;->val$infoValue:Ljava/lang/String;

    invoke-virtual {v0, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 44
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity$1;->val$thisTask:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    const/4 v1, 0x1

    iput-boolean v1, v0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->postedToUI:Z

    .line 48
    return-void
.end method
