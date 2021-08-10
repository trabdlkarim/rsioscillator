#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import click
from rsioscillator import datasource as ds
from rsioscillator import rsi
from rsioscillator import VERSION
@click.command()
@click.version_option(version=VERSION, prog_name="rsioscillator")
@click.argument('excel') 
def main(excel):    
    data = ds.read_excel(excel)
    data = ds.process_data(data)
    data['RSI-14'] = rsi.compute_ewm_rsi(data['Close'])
    data = data.dropna()
    click.echo("Data First 5 Records")
    click.echo("====================")
    print(data.head())
    #rsi.rsi_plot(data)
    rsi.rsi_plot_with_signals(data) 

if __name__ == "__main__":
    main(sys.argv[1:])