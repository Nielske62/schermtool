import requests
import numpy as np
from configuratie import rekeningenfile
from accountfile import gebruikersnaam, wachtwoord

def pakdata(dy, dm, dd, dh, dn, py, pm, pd, ph, pn):
    with requests.Session() as s:
        r = s.get('https://admin.twelve.eu')
        WBF_offset = r.text.find('id="WBF_ValidationCode" value="')+31
        WBF_Validationjetser = r.text[WBF_offset:WBF_offset+36]
        
        payload = {
            'usr_login': gebruikersnaam,
            'usr_password': wachtwoord,
            'language': 'nl-NL',
            'urlRef': '/scripts/admin/report_edit.aspx?strTab=rbsd&clt_id=3020',
            'WBF_ValidationCode': WBF_Validationjetser
    }
        payload2 = {
            'clt_id': 3020,
            'strTab': 'rbsd', 
            'blnExport': 0,
            'blnDateSpanTransactions': 1,
            'rfr_id': '',
            'blnDateSpanTransactions': 'true', 
            'report_date_begin_d': pd,
            'report_date_begin_m': pm,
            'report_date_begin_y': py,
            'report_time_begin_h': ph,
            'report_time_begin_n': pn,
            'report_date_end_d': dd,
            'report_date_end_m': dm,
            'report_date_end_y': dy,
            'report_time_end_h': dh,
            'report_time_end_n': dn 
        }
        
        
        p = s.get("https://admin.twelve.eu/scripts/login_post.aspx", data=payload)
        pagina = s.get('https://admin.twelve.eu/scripts/admin/report_edit.aspx?strTab=rbsd&clt_id=3020', data=payload2)
        s.close()
        
    return pagina.content.splitlines()

def nummerscommissies():
    f = np.genfromtxt(rekeningenfile, skip_header=1, delimiter=";")
    return f

    
