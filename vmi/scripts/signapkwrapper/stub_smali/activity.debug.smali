# virtual methods
.method public onCreate(Landroid/os/Bundle;)V
    .locals 3

    .prologue
    
    # Call original onCreate
    invoke-direct {p0, p1}, $ACTIVITY_CLASS_NAME$->onCreateOrig(Landroid/os/Bundle;)V
    
    # Invoke WrapperDebug
    # p0 is the Activity, DO NOT touch.
    const-string v0, "WrapperDebug"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Class: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I
    
    return-void
.end method

