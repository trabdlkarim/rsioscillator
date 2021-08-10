#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pathlib
import pytest
from rsioscillator.datasource import read_excel, fetch_alphavantage_data

@pytest.fixture
def path():
    root = pathlib.Path('__FILE__').parent.resolve()
    return str(root / 'data/X30YVADE.xlsx')

def test_read_excel(path):
    df = read_excel(path)
    assert len(df.head()) == 5
    
def test_fetch_alphavantage_data():
    df = fetch_alphavantage_data('IBM', '2021-01-01')
    assert len(df.head()) == 5