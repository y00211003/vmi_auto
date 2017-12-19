.class public Lcom/trendmicro/vmi/jni/QemudCommunicationJni;
.super Ljava/lang/Object;
.source "QemudCommunicationJni.java"


# static fields
.field private static final LOG_TAG:Ljava/lang/String; = "QemudCommunicationJni"

.field private static instance:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;


# direct methods
.method static constructor <clinit>()V
    .registers 3

    .prologue
    .line 27
    :try_start_0
    const-string v1, "qemud_communication_jni"

    invoke-static {v1}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    .line 28
    const-string v1, "QemudCommunicationJni"

    const-string v2, "load qemud_communication_jni library success"

    invoke-static {v1, v2}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    :try_end_c
    .catch Ljava/lang/UnsatisfiedLinkError; {:try_start_0 .. :try_end_c} :catch_d

    .line 33
    .local v0, "e":Ljava/lang/UnsatisfiedLinkError;
    :goto_c
    return-void

    .line 29
    .end local v0    # "e":Ljava/lang/UnsatisfiedLinkError;
    :catch_d
    move-exception v0

    .line 30
    .restart local v0    # "e":Ljava/lang/UnsatisfiedLinkError;
    invoke-virtual {v0}, Ljava/lang/UnsatisfiedLinkError;->printStackTrace()V

    .line 31
    const-string v1, "QemudCommunicationJni"

    const-string v2, "load qemud_communication_jni library failed"

    invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_c
.end method

.method private constructor <init>()V
    .registers 1

    .prologue
    .line 65
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 67
    return-void
.end method

.method public static getInstance()Lcom/trendmicro/vmi/jni/QemudCommunicationJni;
    .registers 1

    .prologue
    .line 70
    sget-object v0, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->instance:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    if-nez v0, :cond_b

    .line 71
    new-instance v0, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    invoke-direct {v0}, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;-><init>()V

    sput-object v0, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->instance:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    .line 73
    :cond_b
    sget-object v0, Lcom/trendmicro/vmi/jni/QemudCommunicationJni;->instance:Lcom/trendmicro/vmi/jni/QemudCommunicationJni;

    return-object v0
.end method


# virtual methods
.method public native qemudClose(I)V
.end method

.method public native qemudOpen(Ljava/lang/String;)I
.end method

.method public native qemudReceive(I)Ljava/lang/String;
.end method

.method public native qemudSend(ILjava/lang/String;I)I
.end method
