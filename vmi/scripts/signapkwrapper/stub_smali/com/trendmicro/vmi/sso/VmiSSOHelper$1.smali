.class Lcom/trendmicro/vmi/sso/VmiSSOHelper$1;
.super Ljava/util/TimerTask;
.source "VmiSSOHelper.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/trendmicro/vmi/sso/VmiSSOHelper;->getSSOInfoFromUnia(Landroid/content/Context;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

.field private final synthetic val$vsoDataGetTask:Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;


# direct methods
.method constructor <init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;)V
    .registers 3

    .prologue
    .line 1
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    iput-object p2, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper$1;->val$vsoDataGetTask:Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;

    .line 90
    invoke-direct {p0}, Ljava/util/TimerTask;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 3

    .prologue
    .line 92
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    invoke-virtual {v0}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->dismissProgressDialog()V

    .line 93
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isInitialized()Z

    move-result v0

    if-nez v0, :cond_18

    .line 95
    const-string v0, "VMIWrapper"

    const-string v1, "Cancel task!"

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 97
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper$1;->val$vsoDataGetTask:Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->cancel(Z)Z

    .line 99
    :cond_18
    return-void
.end method
