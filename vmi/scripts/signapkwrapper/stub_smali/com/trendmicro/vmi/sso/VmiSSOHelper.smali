.class public Lcom/trendmicro/vmi/sso/VmiSSOHelper;
.super Ljava/lang/Object;
.source "VmiSSOHelper.java"


# static fields
.field public static final LOG_TAG:Ljava/lang/String; = "VMIWrapper"


# instance fields
.field private activityTarget:Landroid/app/Activity;

.field private context:Landroid/content/Context;

.field private mapInfoKey:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/Integer;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private progressDlg:Landroid/app/ProgressDialog;

.field private viewTarget:Landroid/view/View;


# direct methods
.method public constructor <init>()V
    .registers 2

    .prologue
    const/4 v0, 0x0

    .line 35
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 27
    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    .line 29
    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->mapInfoKey:Ljava/util/Map;

    .line 31
    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->context:Landroid/content/Context;

    .line 32
    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->activityTarget:Landroid/app/Activity;

    .line 33
    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->viewTarget:Landroid/view/View;

    .line 37
    return-void
.end method

.method private fillSSOInfoToUi(Landroid/app/Activity;Landroid/view/View;)V
    .registers 15
    .param p1, "activityTarget"    # Landroid/app/Activity;
    .param p2, "viewTarget"    # Landroid/view/View;

    .prologue
    .line 121
    iget-object v10, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->mapInfoKey:Ljava/util/Map;

    invoke-interface {v10}, Ljava/util/Map;->entrySet()Ljava/util/Set;

    move-result-object v5

    .line 122
    .local v5, "setEntries":Ljava/util/Set;, "Ljava/util/Set<Ljava/util/Map$Entry<Ljava/lang/Integer;Ljava/lang/String;>;>;"
    invoke-interface {v5}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    move-result-object v4

    .line 123
    .local v4, "iterEntry":Ljava/util/Iterator;, "Ljava/util/Iterator<Ljava/util/Map$Entry<Ljava/lang/Integer;Ljava/lang/String;>;>;"
    :goto_a
    invoke-interface {v4}, Ljava/util/Iterator;->hasNext()Z

    move-result v10

    if-nez v10, :cond_11

    .line 162
    return-void

    .line 124
    :cond_11
    invoke-interface {v4}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/util/Map$Entry;

    .line 125
    .local v2, "entry":Ljava/util/Map$Entry;, "Ljava/util/Map$Entry<Ljava/lang/Integer;Ljava/lang/String;>;"
    invoke-interface {v2}, Ljava/util/Map$Entry;->getKey()Ljava/lang/Object;

    move-result-object v10

    check-cast v10, Ljava/lang/Integer;

    invoke-virtual {v10}, Ljava/lang/Integer;->intValue()I

    move-result v3

    .line 126
    .local v3, "idControl":I
    invoke-interface {v2}, Ljava/util/Map$Entry;->getValue()Ljava/lang/Object;

    move-result-object v6

    check-cast v6, Ljava/lang/String;

    .line 128
    .local v6, "strInfoKey":Ljava/lang/String;
    const/4 v9, 0x0

    .line 133
    .local v9, "tvTarget":Landroid/widget/TextView;
    if-eqz p1, :cond_38

    .line 135
    invoke-virtual {p1, v3}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;

    move-result-object v9

    .end local v9    # "tvTarget":Landroid/widget/TextView;
    check-cast v9, Landroid/widget/TextView;

    .line 136
    .restart local v9    # "tvTarget":Landroid/widget/TextView;
    new-instance v0, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;

    invoke-direct {v0, p0, p1, v3, v6}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;-><init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;Landroid/app/Activity;ILjava/lang/String;)V

    .line 138
    .local v0, "dataFillForActivity":Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;
    invoke-virtual {v0}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;->arrageDataFillTask()V

    .line 140
    .end local v0    # "dataFillForActivity":Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForActivity;
    :cond_38
    if-eqz p2, :cond_48

    .line 142
    invoke-virtual {p2, v3}, Landroid/view/View;->findViewById(I)Landroid/view/View;

    move-result-object v9

    .end local v9    # "tvTarget":Landroid/widget/TextView;
    check-cast v9, Landroid/widget/TextView;

    .line 143
    .restart local v9    # "tvTarget":Landroid/widget/TextView;
    new-instance v1, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;

    invoke-direct {v1, p0, p2, v3, v6}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;-><init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;Landroid/view/View;ILjava/lang/String;)V

    .line 145
    .local v1, "dataFillForView":Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;
    invoke-virtual {v1}, Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;->arrageDataFillTask()V

    .line 149
    .end local v1    # "dataFillForView":Lcom/trendmicro/vmi/sso/VmiSSODataFillTaskForView;
    :cond_48
    new-instance v10, Ljava/lang/Integer;

    invoke-direct {v10, v3}, Ljava/lang/Integer;-><init>(I)V

    invoke-virtual {v10}, Ljava/lang/Integer;->toString()Ljava/lang/String;

    move-result-object v7

    .line 150
    .local v7, "strToast":Ljava/lang/String;
    new-instance v10, Ljava/lang/StringBuilder;

    invoke-static {v7}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v11

    invoke-direct {v10, v11}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v11, " => "

    invoke-virtual {v10, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v10

    invoke-virtual {v10, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v10

    const-string v11, " => "

    invoke-virtual {v10, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v10

    invoke-virtual {v10}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    .line 151
    if-eqz v9, :cond_85

    invoke-virtual {v9}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v8

    .line 154
    .local v8, "strTvTarget":Ljava/lang/String;
    :goto_74
    new-instance v10, Ljava/lang/StringBuilder;

    invoke-static {v7}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v11

    invoke-direct {v10, v11}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v10, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v10

    invoke-virtual {v10}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    goto :goto_a

    .line 152
    .end local v8    # "strTvTarget":Ljava/lang/String;
    :cond_85
    const-string v8, "null"

    goto :goto_74
.end method

.method private makeProgressDialog()V
    .registers 5

    .prologue
    const/4 v3, 0x0

    const/4 v2, 0x1

    .line 44
    new-instance v0, Landroid/app/ProgressDialog;

    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->context:Landroid/content/Context;

    invoke-direct {v0, v1}, Landroid/app/ProgressDialog;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    .line 45
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    invoke-virtual {v0, v2}, Landroid/app/ProgressDialog;->setProgressStyle(I)V

    .line 50
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    invoke-virtual {v0, v3}, Landroid/app/ProgressDialog;->setProgressNumberFormat(Ljava/lang/String;)V

    .line 51
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    invoke-virtual {v0, v3}, Landroid/app/ProgressDialog;->setProgressPercentFormat(Ljava/text/NumberFormat;)V

    .line 52
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    invoke-virtual {v0, v2}, Landroid/app/ProgressDialog;->setIndeterminate(Z)V

    .line 54
    return-void
.end method


# virtual methods
.method public dismissProgressDialog()V
    .registers 2

    .prologue
    .line 69
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    if-eqz v0, :cond_9

    .line 70
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    invoke-virtual {v0}, Landroid/app/ProgressDialog;->dismiss()V

    .line 72
    :cond_9
    return-void
.end method

.method public getContext()Landroid/content/Context;
    .registers 2

    .prologue
    .line 40
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->context:Landroid/content/Context;

    return-object v0
.end method

.method public getSSOInfoFromUnia(Landroid/content/Context;)V
    .registers 11
    .param p1, "ctx"    # Landroid/content/Context;

    .prologue
    .line 80
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->context:Landroid/content/Context;

    .line 81
    invoke-direct {p0}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->makeProgressDialog()V

    .line 83
    new-instance v4, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;

    invoke-direct {v4, p0}, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;-><init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;)V

    .line 86
    .local v4, "vsoDataGetTask":Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;
    invoke-virtual {p0}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->showProgressDialog()V

    .line 87
    const/4 v6, 0x0

    new-array v6, v6, [Ljava/lang/Void;

    invoke-virtual {v4, v6}, Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;->execute([Ljava/lang/Object;)Landroid/os/AsyncTask;

    .line 89
    new-instance v3, Ljava/util/Timer;

    invoke-direct {v3}, Ljava/util/Timer;-><init>()V

    .line 90
    .local v3, "timer":Ljava/util/Timer;
    new-instance v2, Lcom/trendmicro/vmi/sso/VmiSSOHelper$1;

    invoke-direct {v2, p0, v4}, Lcom/trendmicro/vmi/sso/VmiSSOHelper$1;-><init>(Lcom/trendmicro/vmi/sso/VmiSSOHelper;Lcom/trendmicro/vmi/sso/VmiSSODataGetTask;)V

    .line 103
    .local v2, "task":Ljava/util/TimerTask;
    sget-object v1, Lcom/trendmicro/vmi/sso/VmiSSOData;->STUB_WAIT_TIME:Ljava/lang/String;

    .line 104
    .local v1, "strStubWaitTime":Ljava/lang/String;
    const/16 v5, 0xbb8

    .line 106
    .local v5, "waitTime":I
    :try_start_21
    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I
    :try_end_24
    .catch Ljava/lang/Exception; {:try_start_21 .. :try_end_24} :catch_44

    move-result v5

    .line 111
    :goto_25
    const-string v6, "VMIWrapper"

    new-instance v7, Ljava/lang/StringBuilder;

    const-string v8, "Wait "

    invoke-direct {v7, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v7, v5}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v7

    const-string v8, "ms!"

    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    invoke-static {v6, v7}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 112
    int-to-long v6, v5

    invoke-virtual {v3, v2, v6, v7}, Ljava/util/Timer;->schedule(Ljava/util/TimerTask;J)V

    .line 113
    return-void

    .line 107
    :catch_44
    move-exception v0

    .line 108
    .local v0, "ex":Ljava/lang/Exception;
    const/16 v5, 0xbb8

    goto :goto_25
.end method

.method protected setSSOInfo()V
    .registers 3

    .prologue
    .line 168
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isInitialized()Z

    move-result v0

    if-eqz v0, :cond_1d

    .line 170
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->activityTarget:Landroid/app/Activity;

    if-eqz v0, :cond_11

    .line 171
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->activityTarget:Landroid/app/Activity;

    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->mapInfoKey:Ljava/util/Map;

    invoke-virtual {p0, v0, v1}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->setSSOInfo(Landroid/app/Activity;Ljava/util/Map;)V

    .line 174
    :cond_11
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->viewTarget:Landroid/view/View;

    if-eqz v0, :cond_1c

    .line 175
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->viewTarget:Landroid/view/View;

    iget-object v1, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->mapInfoKey:Ljava/util/Map;

    invoke-virtual {p0, v0, v1}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->setSSOInfo(Landroid/view/View;Ljava/util/Map;)V

    .line 182
    :cond_1c
    :goto_1c
    return-void

    .line 180
    :cond_1d
    invoke-virtual {p0}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->dismissProgressDialog()V

    goto :goto_1c
.end method

.method public setSSOInfo(Landroid/app/Activity;Ljava/util/Map;)V
    .registers 4
    .param p1, "activityTarget"    # Landroid/app/Activity;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/app/Activity;",
            "Ljava/util/Map",
            "<",
            "Ljava/lang/Integer;",
            "Ljava/lang/String;",
            ">;)V"
        }
    .end annotation

    .prologue
    .line 195
    .local p2, "mapInfoKey":Ljava/util/Map;, "Ljava/util/Map<Ljava/lang/Integer;Ljava/lang/String;>;"
    iput-object p2, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->mapInfoKey:Ljava/util/Map;

    .line 196
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->activityTarget:Landroid/app/Activity;

    .line 198
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isInitialized()Z

    move-result v0

    if-nez v0, :cond_e

    .line 199
    invoke-virtual {p0, p1}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->getSSOInfoFromUnia(Landroid/content/Context;)V

    .line 203
    :goto_d
    return-void

    .line 201
    :cond_e
    const/4 v0, 0x0

    invoke-direct {p0, p1, v0}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->fillSSOInfoToUi(Landroid/app/Activity;Landroid/view/View;)V

    goto :goto_d
.end method

.method public setSSOInfo(Landroid/view/View;Ljava/util/Map;)V
    .registers 4
    .param p1, "viewTarget"    # Landroid/view/View;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/view/View;",
            "Ljava/util/Map",
            "<",
            "Ljava/lang/Integer;",
            "Ljava/lang/String;",
            ">;)V"
        }
    .end annotation

    .prologue
    .line 215
    .local p2, "mapInfoKey":Ljava/util/Map;, "Ljava/util/Map<Ljava/lang/Integer;Ljava/lang/String;>;"
    iput-object p1, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->viewTarget:Landroid/view/View;

    .line 216
    iput-object p2, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->mapInfoKey:Ljava/util/Map;

    .line 218
    invoke-static {}, Lcom/trendmicro/vmi/sso/VmiSSOData;->isInitialized()Z

    move-result v0

    if-nez v0, :cond_12

    .line 219
    invoke-virtual {p1}, Landroid/view/View;->getContext()Landroid/content/Context;

    move-result-object v0

    invoke-virtual {p0, v0}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->getSSOInfoFromUnia(Landroid/content/Context;)V

    .line 223
    :goto_11
    return-void

    .line 221
    :cond_12
    const/4 v0, 0x0

    invoke-direct {p0, v0, p1}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->fillSSOInfoToUi(Landroid/app/Activity;Landroid/view/View;)V

    goto :goto_11
.end method

.method public showProgressDialog()V
    .registers 2

    .prologue
    .line 60
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    if-eqz v0, :cond_9

    .line 61
    iget-object v0, p0, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->progressDlg:Landroid/app/ProgressDialog;

    invoke-virtual {v0}, Landroid/app/ProgressDialog;->show()V

    .line 63
    :cond_9
    return-void
.end method
