#!/usr/bin/env python
# encoding: utf-8

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


import logging
import json
import os
import urlparse

from suds.client import Client
import xmltodict


MAX_CHECK_COUNT = 5
logger = logging.getLogger(__name__)
_current_path = os.path.dirname(os.path.realpath(__file__))
_wsdl = os.path.join(_current_path, 'NciicServices.wsdl')
_url = urlparse.urljoin('file://', _wsdl)
_inlicense = r'?v?zQ8>)V:?[ae7_:TACB0(R.F?c/f`+`{c)>i?[7_]VM`QH&Sca/DF\?c?oYpRj`0+/?z?xOW>cTrEdb\OaUuVnb6?x.lGl[.`4[/Df_kTlAg?x1fB/RyV[Hd-;%i?f4ba$?h7s?jPuIx^eUk0g?v@tPrCaW;&r?m?f?h<b?g?v?jXxMnXkNa?x?vLwA/A.^y?x*%D`0A:FGN3$={P9?/6v=h2x?/?v$sFiNmGgRw?x7sRc@xYaaCXhOzcXBm?xSo)r?g<f`+?g?v)m[s@xRxSzEl\;]hSe/k?vA.Tb?j?x?v?jOyaCXo`CGg@gTl@h7/?vL[V;cXPm_w[ra3d=[qVjQp?x=xJdYgb0Tj?x8s?h&;4z?v1pXpJoUiSe?xd%?jaCZ[Rz_/V[Cz^u_w[qc4Ag/k1f?jS[DfIa@nDad<[p.j'
# _inlicense = r'rjszrjsz65236_3054.txt'
_url1 = 'https://ws.nciic.org.cn/nciic_ws/services/NciicServices?wsdl'
_client = Client(_url1)


def _init_inconditions(dict_data):
    rows = {
        "ROWS": {
            "INFO": {"SBM": u"北京神州瑞景科技有限公司"},
            "ROW": [
                {"GMSFHM": u"公民身份号码",
                 "XM": u"姓名"},
                {"GMSFHM": dict_data['id_number'],
                 "XM": dict_data['name'],
                 "@FSD": u'110118',
                 "@YWLX": '实名认证'}
            ]
        }
    }
    return xmltodict.unparse(rows)


def _parse_result(resp_xml):
    result = xmltodict.parse(resp_xml, encoding='utf-8')
    if 'RESPONSE' in result:
        error_xml = json.dumps(result['RESPONSE'], ensure_ascii=False)
        logger.error('NciicServiceError:' + error_xml)
        raise('NCIIC_SERVICE_ERROR', error_xml)
    else:
        row = result['ROWS']['ROW']
        items = row['OUTPUT']['ITEM']
        if 'gmsfhm' in items[0]:
            if items[0]['result_gmsfhm'] == items[1]['result_xm']:
                return True
            else:
                logger.info('CERTIFY_FAILED:' +
                            json.dumps(row, ensure_ascii=False))
                return False
        elif 'errormesage' in items[0]:
            # 我真不想吐槽这个mesage单词了
            logger.info('CERTIFY_FAILED:' +
                        json.dumps(row, ensure_ascii=False))
            return False


def nciic_check(dict_data):
    incondition = _init_inconditions(dict_data)
    print incondition
    resp_xml = _client.service.nciicCheck(_inlicense, incondition)
    return _parse_result(resp_xml)
