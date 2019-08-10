#!/usr/bin/env python3

from aws_cdk import core

from awscdk_py.awscdk_py_stack import AwscdkPyStack


app = core.App()
AwscdkPyStack(app, "awscdk-py")

app.synth()
