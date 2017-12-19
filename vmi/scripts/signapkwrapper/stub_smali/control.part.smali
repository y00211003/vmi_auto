    
    # Add control id to map
    const v2, $CONTROL_ID$

    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    const-string v3, $DATA_KEY$

    invoke-interface {v1, v2, v3}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    
    $ADD_CONTROL_VALUE$
    