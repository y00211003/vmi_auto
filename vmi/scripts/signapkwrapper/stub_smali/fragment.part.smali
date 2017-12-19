# virtual methods
.method public onCreateView(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;
    .locals 4

    .prologue
    
    # Call original onCreateView
    $INVOKE_METHOD$ {p0, p1, p2, p3}, $FRAGMENT_CLASS_NAME$->onCreateViewOrig(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;

    move-result-object v0
    
    # Invoke VmiSSOHelper
    # v0 is the View, v1 is the Map, DO NOT touch.
    # Prepare id->key map
    new-instance v1, Ljava/util/HashMap;

    invoke-direct {v1}, Ljava/util/HashMap;-><init>()V
    
    # Put values
    $ADD_CONTROL_VALUE$
    
    # Call
    new-instance v2, Lcom/trendmicro/vmi/sso/VmiSSOHelper;

    invoke-direct {v2}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;-><init>()V
    
    invoke-virtual {v2, v0, v1}, Lcom/trendmicro/vmi/sso/VmiSSOHelper;->setSSOInfo(Landroid/view/View;Ljava/util/Map;)V

    return-object v0
.end method

