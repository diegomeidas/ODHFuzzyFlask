from model.odhModel import getOdh as odhModel


def getOdh(psi, ass, amp, tra, cic, esp, ali):

    ret = odhModel(psi, ass, amp, tra, cic, esp, ali)
    if ret['status'] == 0: 
        return getResponse(400, "O parametro ("+ str(ret['msg']) +") é obrigatorio")
    else: 
        return getResponse(200, "Ok", "data", ret['msg'])


def getResponse(status, mensagem, nome_do_conteudo=False, conteudo=False):
    
    response = {}
    response["status"] = status
    response["mensagem"] = mensagem

    if nome_do_conteudo and conteudo:
        response[nome_do_conteudo] = conteudo    
        return response
    else:
        return response




