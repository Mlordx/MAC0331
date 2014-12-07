#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from geocomp.common.polygon import Polygon
from geocomp.common import prim
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.guiprim import *
from geocomp import config
from geocomp.common.point import Point

"""
def eReflexo(p,pontos):
    if(p[1] != len(pontos) - 1): prox = p[1] + 1
    else: prox = 0

    if(p[1] != 0): ant = p[1] - 1
    else: ant = len(pontos) - 1

    if(left(pontos[ant],pontos[prox],p): return True
    
    return False
"""

def hertelMehlhorn(l):
           
