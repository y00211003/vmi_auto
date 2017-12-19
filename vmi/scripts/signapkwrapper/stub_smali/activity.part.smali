# virtual methods
.method public onCreate(Landroid/os/Bundle;)V
    .locals 4

    .prologue
    
    # Call original onCreate
    $INVOKE_METHOD$ {p0, p1}, $ACTIVITY_CLASS_NAME$->onCreateOrig(Landroid/os/Bundle;)V
    
    # Invoke VmiSSOHelper
    # p0 is the Activity, v1 is the Map, DO NOT touch.
    # Prepare id->key map
    new-instance v1, Ljava/util/HashMap;

    invoke-direct {v1}, Ljava/util/HashMap;-><init>()V
    
    # Put values
    $ADD_CONTROL_VALUE$
    
    # Call
    new-instance v2, Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    invoke-direct {v2}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;-><init>()V
    
    invoke-virtual {v2, p0, v1}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->setSSOInfo(Landroid/app/Activity;Ljava/util/Map;)V
    
    return-void
.end method

