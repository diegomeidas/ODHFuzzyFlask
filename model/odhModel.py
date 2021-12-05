import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def getOdh(psi, ass, amp, tra, cic, esp, ali):
    
    res = {}
    res['msg'] = getBody(psi, ass, amp, tra, cic, esp, ali)

    if res['msg'] != '': 
        res['status'] = 0
        return res
    else:
        ODH_simulador = setDefinitions()
        return fuzzy(ODH_simulador, psi, ass, amp, tra, cic, esp, ali)

        

def getBody(psi, ass, amp, tra, cic, esp, ali):
    
    ret = ''
    if psi == '' : ret = 'psicolicas'    
    if ass == '' : ret = 'assistencia'
    if amp == '' : ret = 'amparo' 
    if tra == '' : ret = 'transporte' 
    if cic == '' : ret = 'ciclovia' 
    if esp == '' : ret = 'esporte' 
    if ali == '' : ret = 'alimento' 
    return ret

def setDefinitions():
    esporte = ctrl.Antecedent(np.arange(0, 11, 1), 'esporte')
    psicologicas = ctrl.Antecedent(np.arange(0, 11, 1), 'psicologicas')
    assistencia = ctrl.Antecedent(np.arange(0, 11, 1), 'assistencia')
    amparo = ctrl.Antecedent(np.arange(0, 11, 1), 'amparo')
    transporte = ctrl.Antecedent(np.arange(0, 11, 1), 'transporte')
    ciclovia = ctrl.Antecedent(np.arange(0, 11, 1), 'ciclovia')
    alimento = ctrl.Antecedent(np.arange(0, 11, 1), 'alimento')
    ODH = ctrl.Consequent(np.arange(0, 31, 1), 'ODH')

    esporte.automf(names=['baixa', 'media', 'alta'])
    psicologicas.automf(names=['baixa', 'media', 'alta'])
    assistencia.automf(names=['baixa', 'media', 'alta'])
    amparo.automf(names=['baixa', 'media', 'alta'])
    transporte.automf(names=['baixa', 'media', 'alta'])
    ciclovia.automf(names=['baixa', 'media', 'alta'])

    alimento['baixa'] = fuzz.trapmf(alimento.universe, [0, 0, 2,5])
    alimento['media'] = fuzz.trimf(alimento.universe, [2,5,8])
    alimento['alta'] = fuzz.trapmf(alimento.universe, [5,8,10,10])

    ODH['Muito Baixo'] = fuzz.trimf(ODH.universe, [0,0,5])
    ODH['Baixo'] = fuzz.trimf(ODH.universe,       [0,5,10])
    ODH['Medio1'] = fuzz.trimf(ODH.universe,      [5,10,15])
    ODH['Medio2'] = fuzz.trimf(ODH.universe,      [10,15,20])
    ODH['Medio3'] = fuzz.trimf(ODH.universe,      [15,20,25])
    ODH['Alto'] = fuzz.trimf(ODH.universe,        [20,25,30])
    ODH['Muito Alto'] = fuzz.trimf(ODH.universe,  [25,30,30])

    rule1 = ctrl.Rule(alimento['alta'] | esporte['alta'], ODH['Alto'])
    rule2 = ctrl.Rule(alimento['media'], ODH['Medio1'])
    rule3 = ctrl.Rule(alimento['baixa'] & esporte['baixa'], ODH['Baixo'])
    rule4 = ctrl.Rule(alimento['media'] & esporte['baixa'], ODH['Medio2'])
    rule5 = ctrl.Rule(alimento['baixa'] & esporte['media'], ODH['Baixo'])
    rule6 = ctrl.Rule(alimento['baixa'] & esporte['media'] & ciclovia['media'], ODH['Baixo'])
    rule7 = ctrl.Rule(alimento['baixa'] & esporte['alta'] & ciclovia['alta'], ODH['Medio1'])
    rule8 = ctrl.Rule(alimento['baixa'] & esporte['baixa'] & psicologicas['baixa'] & assistencia['baixa'] & amparo['baixa'] & transporte['baixa'] & ciclovia['baixa'], ODH['Muito Baixo'])
    rule9 = ctrl.Rule(alimento['media'] & esporte['media'] & psicologicas['media'] & assistencia['media'] & amparo['media'] & transporte['media'] & ciclovia['media'], ODH['Medio2'])
    rule10 = ctrl.Rule(alimento['alta'] & esporte['alta'] & psicologicas['alta'] & assistencia['alta'] & amparo['alta'] & transporte['alta'] & ciclovia['alta'], ODH['Muito Alto'])

    ODH_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
    ODH_sim = ctrl.ControlSystemSimulation(ODH_ctrl)
    return ODH_sim


def fuzzy(ODH_simulador, psi, ass, amp, tra, cic, esp, ali):  
    
    result = {}

    ODH_simulador.input['psicologicas'] = int(psi)
    ODH_simulador.input['assistencia'] = int(ass)
    ODH_simulador.input['amparo'] = int(amp)
    ODH_simulador.input['transporte'] = int(tra)
    ODH_simulador.input['ciclovia'] = int(cic)
    ODH_simulador.input['esporte'] = int(esp)
    ODH_simulador.input['alimento'] = int(ali)

    ODH_simulador.compute()

    result['msg'] = str(ODH_simulador.output['ODH'])
    result['status'] = 1
    return result