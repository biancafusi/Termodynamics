#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Este programa é um auxiliar para vertical_v3.py.
Define as Grandezas Termodinâmicas e os Gráficos.
PROGRAMMER(S)
    Bianca F.
REVISION HISTORY
    20230410 -- Initial version created 
    20230511 -- Review and corrected
'''
import numpy as np
import os
from netCDF4 import Dataset, num2date, date2num 
import matplotlib.pyplot as plt
import datetime as dt  
import metpy.calc  as calc
import metpy.constants as const
from metpy.units import units
from metpy.plots import SkewT

SAVE_FOLDER = "/home/biancaf/Documents/INPE/Disciplinas/Termo/Aula_P/L3/Images"

DRY_R = 287.0 ## J K^-1 kg^-1
DRY_CP = 1004 # J K^-1 kg^-1
GRAVITY = 9.81 # m/s^2	
MOLECULAR_RATIO = 0.622
LAPSE_RATE = 0.0098 # K/m

def plot_temp(PRESSAO, DATAS, TEMPERATURA, XLABEL, YLABEL, BARRA_LATERAL, TITLE, FILE_NAME):
    '''
    Plot da Temperatura
    '''
    fig, ax = plt.subplots(figsize=(12, 15))  		
    temp_2D = TEMPERATURA.reshape(TEMPERATURA.shape[0], -1)		#reshape to become only z and data
    X, Y = np.meshgrid(DATAS, PRESSAO)
    c = ax.contourf(X, Y, temp_2D.T, cmap='coolwarm')
    ax.set_xlabel(XLABEL)
    ax.set_ylabel(YLABEL)
    cbar = fig.colorbar(c)
    cbar.set_label(BARRA_LATERAL)
    plt.title(TITLE)
    folder_path = SAVE_FOLDER
    file_name = FILE_NAME
    full_path = os.path.join(folder_path, file_name)
    plt.savefig(full_path)

    return 

def plot_prcv(DATAS, PRCV, XLABEL, YLABEL, TITLE, FILE_NAME):
    '''
    Plot da Precipitação e Zoom Precipitação
    '''
    fig, ax = plt.subplots(figsize=(10, 6))  		
    plt.plot(DATAS, PRCV, color='black') 	
    ax.set_xlabel(XLABEL)
    ax.set_ylabel(YLABEL)
    plt.title(TITLE)
    folder_path = SAVE_FOLDER
    file_name = FILE_NAME
    full_path = os.path.join(folder_path, file_name)
    plt.savefig(full_path)

    return

def plot_vertical(GRANDEZA, PRESSAO, XLABEL, YLABEL, TITLE, FILE_NAME):
    '''
    Plot de Perfis Verticais
    '''
    fig, ax = plt.subplots(figsize=(4, 10))  		
    plt.plot(GRANDEZA, PRESSAO, color='black')
    ax.invert_yaxis()
    ax.set_xlabel(XLABEL)
    ax.set_ylabel(YLABEL)
    plt.title(TITLE)
    folder_path = SAVE_FOLDER
    file_name = FILE_NAME
    full_path = os.path.join(folder_path, file_name)
    plt.savefig(full_path)

    return

def plot_comparativo(GRANDEZA1, GRANDEZA2, PRESSAO, LEGENDA_1, LEGENDA_2, XLABEL, YLABEL, TITLE, FILE_NAME):
    '''
    Plot Comparativo
    '''
    fig, ax = plt.subplots(figsize=(4, 10))  		
    ax.invert_yaxis()
    ax.plot(GRANDEZA1, PRESSAO, color='blue', label=LEGENDA_1)
    ax.plot(GRANDEZA2, PRESSAO, color='red', label=LEGENDA_2)
    ax.set_xlabel(XLABEL)
    ax.set_ylabel(YLABEL)
    plt.title(TITLE)
    ax.legend()
    folder_path = SAVE_FOLDER
    file_name = FILE_NAME
    full_path = os.path.join(folder_path, file_name)
    plt.savefig(full_path)

    return

def plot_comparativo_vsTemperatura(GRANDEZA1, GRANDEZA2, TEMPERATURA, LEGENDA_1, LEGENDA_2, XLABEL, YLABEL, TITLE, FILE_NAME):
    '''
    #Plot Comparativo 2
    '''
    fig, ax = plt.subplots(figsize=(4, 10))  		
    ax.invert_yaxis()
    ax.plot(TEMPERATURA, GRANDEZA1, color='blue', label=LEGENDA_1)
    ax.plot(TEMPERATURA, GRANDEZA2, color='red', label=LEGENDA_2)
    ax.set_xlabel(XLABEL)
    ax.set_ylabel(YLABEL)
    plt.title(TITLE)
    ax.legend()
    folder_path = SAVE_FOLDER
    file_name = FILE_NAME
    full_path = os.path.join(folder_path, file_name)
    plt.savefig(full_path)

    return

def calc_temperatura_potencial(RANGE_TEMPERATURE, RANGE_PRESSURE):
    '''
    Temperatura Potencial
    '''
    CALC1 = 1000 / RANGE_PRESSURE
    TEMPERATURA_POTENCIAL = RANGE_TEMPERATURE * (CALC1**(DRY_R / DRY_CP))

    return TEMPERATURA_POTENCIAL

def calc_temperatura_potencial_virtual(VAPOR_PRESSURE, RANGE_PRESSURE, RANGE_TEMPERATURE):
    '''
    Temperatura Potencial Virtual
    '''
    CALC2 = (VAPOR_PRESSURE / RANGE_PRESSURE)*(1 - MOLECULAR_RATIO)
    VIRTUAL_TEMPERATURE = RANGE_TEMPERATURE / (1 - CALC2)

    CALC3 = (1000/RANGE_PRESSURE) **(DRY_R / DRY_CP)
    POTENTIAL_VIRTUAL_TEMPERATURE = VIRTUAL_TEMPERATURE * CALC3

    return POTENTIAL_VIRTUAL_TEMPERATURE

def calc_pressao_vapor(RANGE_PRESSURE, RANGE_SPECIFIC_HUMIDITY):
    '''
    Pressão de Vapor
    '''
    VAPOR_PRESSURE = RANGE_PRESSURE * (RANGE_SPECIFIC_HUMIDITY / (RANGE_SPECIFIC_HUMIDITY + MOLECULAR_RATIO))

    return VAPOR_PRESSURE

def calc_pressao_saturacao(RANGE_TEMPERATURE):
    '''
    Pressão de Vapor de Saturação
    '''
    A = (7.5 * RANGE_TEMPERATURE) / (RANGE_TEMPERATURE + 237.3) #TEMPERATURA EM GRAUS CELSIUS
    SATURATION_VAPOR_PRESSURE = 6.11 * 10**(A)

    return SATURATION_VAPOR_PRESSURE

def calc_umidade_esp_sat(SATURATION_VAPOR_PRESSURE, RANGE_PRESSURE):
    '''
    Umidade Específica de Saturação
    '''
    SATURATION_ESPECIFIC_HUMIDITY = MOLECULAR_RATIO * (SATURATION_VAPOR_PRESSURE / RANGE_PRESSURE)

    return SATURATION_ESPECIFIC_HUMIDITY

def calc_umidade_relativa(RANGE_SPECIFIC_HUMIDITY, SATURATION_ESPECIFIC_HUMIDITY):
    '''
    Umidade Relativa
    '''
    RELATIVE_HUMIDITY = RANGE_SPECIFIC_HUMIDITY / SATURATION_ESPECIFIC_HUMIDITY

    return RELATIVE_HUMIDITY

def calc_densidade(RANGE_PRESSURE, VAPOR_PRESSURE, RANGE_TEMPERATURE):
    '''
    Densidade do Ar
    '''
    CALC2 = (VAPOR_PRESSURE / RANGE_PRESSURE)*(1 - MOLECULAR_RATIO)
    VIRTUAL_TEMPERATURE = RANGE_TEMPERATURE / (1 - CALC2)

    DENSITY = (RANGE_PRESSURE / 0.01) / (287 * VIRTUAL_TEMPERATURE) #Dividi por 0.01 para converter mbar into Pa

    return DENSITY

def calc_temperatura_pot_equi(RANGE_LATENT_HEAT, SATURATION_ESPECIFIC_HUMIDITY, RANGE_TEMPERATURE, POTENTIAL_TEMPERATURE):
    '''
    Temperatura Potencial Equivalente
    '''
    FRACTION = (RANGE_LATENT_HEAT * SATURATION_ESPECIFIC_HUMIDITY) / (DRY_CP * RANGE_TEMPERATURE)
    POTENTIAL_EQUIVALENT_TEMPERATURE = POTENTIAL_TEMPERATURE * np.exp(FRACTION)

    return POTENTIAL_EQUIVALENT_TEMPERATURE

def calc_energia_est_seca(RANGE_PRESSURE, TEMPERATURE_SURFACE, RANGE_TEMPERATURE):
    '''
    Energia Estática Seca
    '''
    FRACTION1 = (RANGE_PRESSURE / 1000)**(LAPSE_RATE * DRY_R / GRAVITY)
    HEIGHT = (TEMPERATURE_SURFACE / LAPSE_RATE) * (1 - FRACTION1)

    DRY_STATIC_ENERGY = DRY_CP * RANGE_TEMPERATURE + GRAVITY * HEIGHT #J/kg - talvez fique melhor mostrando em k

    return DRY_STATIC_ENERGY

def calc_energia_est_umida_sat(SATURATION_ESPECIFIC_HUMIDITY, RANGE_TEMPERATURE, RANGE_SPECIFIC_HUMIDITY, \
                          RANGE_PRESSURE, TEMPERATURE_SURFACE, RANGE_LATENT_HEAT):
    '''
    Energia Estática Úmida e Saturada
    '''
    FRACTION1 = (RANGE_PRESSURE / 1000)**(LAPSE_RATE * DRY_R / GRAVITY)
    HEIGHT = (TEMPERATURE_SURFACE / LAPSE_RATE) * (1 - FRACTION1)

    SATURATED_MOIST_STATIC_ENERGY = DRY_CP* RANGE_TEMPERATURE + RANGE_SPECIFIC_HUMIDITY * HEIGHT + RANGE_LATENT_HEAT * \
        SATURATION_ESPECIFIC_HUMIDITY #J/kg - talvez fique melhor mostrando em kJ
    
    return SATURATED_MOIST_STATIC_ENERGY

def plot_SKEWT(RANGE_PRESSURE, RANGE_TEMPERATURE, RANGE_SPECIFIC_HUMIDITY, SURFACE_TEMPERATURE, SURFACE_PRESSURE):

    DEW_TEMPERATURE = calc.dewpoint_from_specific_humidity(RANGE_PRESSURE, RANGE_TEMPERATURE, RANGE_SPECIFIC_HUMIDITY)
    INITIAL_DEW_TEMPERATURE = DEW_TEMPERATURE[0]
    PARCEL_PROFILE = calc.parcel_profile(RANGE_PRESSURE, SURFACE_TEMPERATURE, INITIAL_DEW_TEMPERATURE).to('degC') 
    
    fig = plt.figure(figsize=(8.27, 14)) 
    skew = SkewT(fig, rotation=45) # coloca as isotermas em 45 graus e as isobaras horizontal
    skew.ax.set_xlabel(f'Temperature ({PARCEL_PROFILE.units:~P})')
    skew.ax.set_ylabel(f'Pressure ({RANGE_PRESSURE.units:~P})')
    skew.plot_dry_adiabats(colors='orangered', linewidths=1)
    skew.plot_moist_adiabats(colors='tab:green', linewidths=1)
    skew.plot_mixing_lines(colors='dodgerblue', linewidths=1) 
    skew.plot(RANGE_PRESSURE, RANGE_TEMPERATURE, 'r')     # Plot the data using normal plotting functions, in this case using
    skew.plot(RANGE_PRESSURE, DEW_TEMPERATURE, 'g')     # log scaling in Y, as dictated by the typical meteorological plot.
    skew.plot(RANGE_PRESSURE, PARCEL_PROFILE, 'm')     # log scaling in Y, as dictated by the typical meteorological plot.
    
    #Convecção
    lcl_p, lcl_t = calc.lcl(SURFACE_PRESSURE , SURFACE_TEMPERATURE, INITIAL_DEW_TEMPERATURE) #pega a temp em um determinado altura aq no caso é a base em um determinado tempo index
    skew.plot(RANGE_PRESSURE, PARCEL_PROFILE, 'b')
    skew.plot(lcl_p, lcl_t, 'ko', markerfacecolor='black')
    # Shade areas of CAPE and CIN
    skew.shade_cin(RANGE_PRESSURE , RANGE_TEMPERATURE, PARCEL_PROFILE, DEW_TEMPERATURE, color='green')
    skew.shade_cape(RANGE_PRESSURE, RANGE_TEMPERATURE, PARCEL_PROFILE)
    # Add some titles
    plt.title('2014-02-14 20hr', loc='right')
    folder_path = SAVE_FOLDER
    file_name = "SkewT_SEM.pdf"
    full_path = os.path.join(folder_path, file_name)
    plt.savefig(full_path)

    return

def plot_SKEWT(RANGE_PRESSURE, RANGE_TEMPERATURE, RANGE_SPECIFIC_HUMIDITY, SURFACE_TEMPERATURE, SURFACE_PRESSURE):

    DEW_TEMPERATURE = calc.dewpoint_from_specific_humidity(RANGE_PRESSURE, RANGE_TEMPERATURE, RANGE_SPECIFIC_HUMIDITY)
    INITIAL_DEW_TEMPERATURE = DEW_TEMPERATURE[0]
    PARCEL_PROFILE = calc.parcel_profile(RANGE_PRESSURE, SURFACE_TEMPERATURE, INITIAL_DEW_TEMPERATURE).to('degC') 
    
    fig = plt.figure(figsize=(8.27, 14)) 
    skew = SkewT(fig, rotation=45) # coloca as isotermas em 45 graus e as isobaras horizontal
    skew.ax.set_xlabel(f'Temperature ({PARCEL_PROFILE.units:~P})')
    skew.ax.set_ylabel(f'Pressure ({RANGE_PRESSURE.units:~P})')
    skew.plot_dry_adiabats(colors='orangered', linewidths=1)
    skew.plot_moist_adiabats(colors='tab:green', linewidths=1)
    skew.plot_mixing_lines(colors='dodgerblue', linewidths=1) 
    skew.plot(RANGE_PRESSURE, RANGE_TEMPERATURE, 'r')     # Plot the data using normal plotting functions, in this case using
    skew.plot(RANGE_PRESSURE, DEW_TEMPERATURE, 'g')     # log scaling in Y, as dictated by the typical meteorological plot.
    skew.plot(RANGE_PRESSURE, PARCEL_PROFILE, 'm')     # log scaling in Y, as dictated by the typical meteorological plot.
    
    #Convecção
    lcl_p, lcl_t = calc.lcl(SURFACE_PRESSURE , SURFACE_TEMPERATURE, INITIAL_DEW_TEMPERATURE) #pega a temp em um determinado altura aq no caso é a base em um determinado tempo index
    skew.plot(RANGE_PRESSURE, PARCEL_PROFILE, 'b')
    skew.plot(lcl_p, lcl_t, 'ko', markerfacecolor='black')
    # Shade areas of CAPE and CIN
    skew.shade_cin(RANGE_PRESSURE , RANGE_TEMPERATURE, PARCEL_PROFILE, DEW_TEMPERATURE, color='green')
    skew.shade_cape(RANGE_PRESSURE, RANGE_TEMPERATURE, PARCEL_PROFILE)
    # Add some titles
    plt.title('2014-02-27 11hr', loc='right')
    folder_path = SAVE_FOLDER
    file_name = "SkewT_CONV.pdf"
    full_path = os.path.join(folder_path, file_name)
    plt.savefig(full_path)

    return