.class Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;
.super Ljava/util/TimerTask;
.source "VmiSSODataFillTask.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->arrageDataFillTask()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

.field private final synthetic val$infoValue:Ljava/lang/String;


# direct methods
.method constructor <init>(Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;Ljava/lang/String;)V
    .registers 3

    .prologue
    .line 1
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    iput-object p2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->val$infoValue:Ljava/lang/String;

    .line 128
    invoke-direct {p0}, Ljava/util/TimerTask;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .registers 6

    .prologue
    .line 130
    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    iget-object v1, v1, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->infoKey:Ljava/lang/String;

    invoke-static {v1}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->needWaitOtherInfo(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_10

    .line 133
    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    const/4 v2, 0x1

    iput-boolean v2, v1, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->blocked:Z

    .line 148
    :goto_f
    return-void

    .line 137
    :cond_10
    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    iget-boolean v1, v1, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->blocked:Z

    if-eqz v1, :cond_1b

    .line 140
    const-wide/16 v1, 0xfa

    :try_start_18
    invoke-static {v1, v2}, Ljava/lang/Thread;->sleep(J)V
    :try_end_1b
    .catch Ljava/lang/InterruptedException; {:try_start_18 .. :try_end_1b} :catch_2b

    .line 147
    :cond_1b
    :goto_1b
    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    iget-object v2, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    iget v2, v2, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->tvControlId:I

    iget-object v3, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->this$0:Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;

    iget-object v3, v3, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->infoKey:Ljava/lang/String;

    iget-object v4, p0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask$1;->val$infoValue:Ljava/lang/String;

    invoke-virtual {v1, v2, v3, v4}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTask;->postToUi(ILjava/lang/String;Ljava/lang/String;)V

    goto :goto_f

    .line 141
    :catch_2b
    move-exception v0

    .line 142
    .local v0, "e":Ljava/lang/InterruptedException;
    const-string v1, "VMIWrapper"

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v3}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 143
    const-string v3, " sleep failed."

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    .line 142
    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_1b
.end method
