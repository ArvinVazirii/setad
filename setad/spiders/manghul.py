import scrapy
from scrapy.http import FormRequest
import time
import json


class get_manghul(scrapy.Spider):
    name = "manghul"
    start_urls = ["https://eauc.setadiran.ir/eauc/welcome.action?gateway=setad"]
    manghul_url = "https://eauc.setadiran.ir/eauc/mainEstate-Load.action?_search=false&nd={sys_T1}&rows={" \
                  "row_NO}&page=0&sidx=&sord=asc&_={sys_T2} "
    header_FP = {

        'Accept': 'application/json, text/javascript, */*;q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'eauc.setadiran.ir',
        'Referer': 'https://eauc.setadiran.ir/eauc/welcome.action?gateway=setad',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    header_I = {

        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=0000s8v2IeQ3y8QN8zn4B2U_yvI:1erc06b2s;JSESSIONID=0000s8v2IeQ3y8QN8zn4B2U_yvI:1erc06b2s',
        'Host': 'eauc.setadiran.ir',
        'Referer': 'https://eauc.setadiran.ir/eauc/welcome.action?gateway=setad',
        'Origin': 'https://eauc.setadiran.ir',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    data_I = {'auctionId': '', 'backActionName': 'welcome-home-formPart'}

    def parse(self, response):
        yield response.follow(
            url=self.manghul_url.format(sys_T1=int(time.time()), row_NO=100000, sys_T2=int(time.time())),
            callback=self.firstpage, headers=self.header_FP)

    def firstpage(self, response):
        manghul = response.json()['gridModel']
        FP_data = []
        id_auc = []
        for i in manghul:
            auctionNO = i["auctionParty"]["auction"]["auctionNo"]
            auctioneer_city = i["auctionParty"]["auction"]["auctioneer"]['city']['name']
            auctioneer_province = i["auctionParty"]["auction"]["auctioneer"]['city']["province"]['name']
            auctioneer_name = i["auctionParty"]["auction"]["auctioneer"]['name']
            auc_title = i["auctionParty"]["auction"]['title']
            fromproposalDate = i["auctionParty"]["auction"]["fromProposalDate"]
            fromsiteshowDate = i["auctionParty"]["auction"]["fromSiteShowDate"]
            toproposalDate = i["auctionParty"]["auction"]["toProposalDate"]
            tositeshowDate = i["auctionParty"]["auction"]["toSiteShowDate"]
            basetotalprice = i["auctionParty"]["baseTotalPrice"]
            partyNO = i["auctionParty"]["partyNo"]
            state = i["auctionParty"]["state"]
            title = i["auctionParty"]["title"]
            city = i["auctionParty"]["visitCity"]["name"]
            province = i["auctionParty"]["visitCity"]["province"]["name"]
            partyGroups = i["partyGroups"]
            id_auc.append(i["auctionParty"]["auction"]["id"])

            baseinfos = {"id42": auctionNO,
                         "id43": auctioneer_name,
                         "id44": auctioneer_province,
                         "id45": partyNO,
                         "id46": title,
                         "id47": province,
                         "id48": partyGroups,
                         "id49": basetotalprice,
                         "id50": [fromproposalDate, toproposalDate],
                         "id51": [fromsiteshowDate, tositeshowDate],
                         "id52": state
                         }

            FP_data.append(baseinfos)

        yield {"FP_data": FP_data}

        for i in id_auc:
            yield FormRequest(
                url='https://eauc.setadiran.ir/eauc/auctionDetailsViewAction-loadFormPart.action?mainAction_conversation=0',
                callback=self.infos, headers=self.header_I, method='POST',
                formdata={'auctionId': str(i), 'backActionName': 'welcome-home-formPart'})

    def infos(self, response):

        auc_num = response.xpath(
            '''//*[(@id = "auctionDetailsViewAction-loadFormPart_auctionDto_auction_auctionNo")]/@value''').get()
        aucTile = response.xpath('''//*[(@id = "title")]/@value''').get()
        fromsiteshowdate = response.xpath('''//*[(@id = "fromSiteShowDate")]/@value''').get()
        fss_time = response.xpath('''//*[(@id = "fromSiteShowTime")]/@value''').get()
        tositeshowdate = response.xpath('''//*[(@id = "toSiteShowDate")]/@value''').get()
        tss_time = response.xpath('''//*[(@id = "toSiteShowTime")]/@value''').get()
        fromviewdate = response.xpath('''//*[(@id = "fromViewDate")]/@value''').get()
        fv_time = response.xpath('''//*[(@id = "fromViewTime")]/@value''').get()
        toviewdate = response.xpath('''//*[(@id = "toViewDate")]/@value''').get()
        tv_time = response.xpath('''//*[(@id = "toViewTime")]/@value''').get()
        rec_docDate = response.xpath('''//*[(@id = "receiptDocumentDate")]/@value''').get()
        rec_doctime = response.xpath('''//*[(@id = "receiptDocumentTime")]/@value''').get()
        fromproposaldate = response.xpath('''//*[(@id = "fromProposalDate")]/@value''').get()
        fp_time = response.xpath('''//*[(@id = "fromProposalTime")]/@value''').get()
        toproposaldate = response.xpath('''//*[(@id = "toProposalDate")]/@value''').get()
        tp_time = response.xpath('''//*[(@id = "toProposalTime")]/@value''').get()
        openingdate = response.xpath('''//*[(@id = "openingDate")]/@value''').get()
        op_time = response.xpath('''//*[(@id = "openingTime")]/@value''').get()
        winnerannouncedate = response.xpath('''//*[(@id = "winnerAnnounceDate")]/@value''').get()
        wa_time = response.xpath('''//*[(@id = "winnerAnnounceTime")]/@value''').get()
        pay_without = response.xpath(
            '''//tr[(((count(preceding-sibling::*) + 1) = 18) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        winner_ac = response.xpath(
            '''//tr[(((count(preceding-sibling::*) + 1) = 19) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        lastpaytime = response.xpath(
            '''//tr[(((count(preceding-sibling::*) + 1) = 20) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        penalty_pay = response.xpath(
            '''//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        getwarehouse_without = response.xpath(
            '''//tr[(((count(preceding-sibling::*) + 1) = 20) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        getwarhouse = response.xpath(
            '''//tr[(((count(preceding-sibling::*) + 1) = 23) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        penalty_percent = response.xpath(
            '''//tr[(((count(preceding-sibling::*) + 1) = 24) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        days_exist = response.xpath(
            '''//tr[(((count(preceding-sibling::*) + 1) = 24) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        participationcost = response.xpath('''//*[(@id = "participationCost")]/@value''').get()
        receiptdocdate = response.xpath('''//*[(@id = "receiptDocumentDate")]/@value''').get()
        rd_time = response.xpath('''//*[(@id = "receiptDocumentTime")]/@value''').get()
        vadiye_percent = response.xpath(
            '''//td[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "number", " " ))]/@value''').get()
        participateAccountsTxt = response.xpath('''//*[(@id = "participateAccountsTxt")]/@value''').get()
        txtParticipateAccDepoistId = response.xpath('''//*[(@id = "txtParticipateAccDepoistId")]/@value''').get()
        trustAccountsTxt = response.xpath('''//*[(@id = "trustAccountsTxt")]/@value''').get()
        txtTrustAccDepoistId = response.xpath('''//*[(@id = "txtTrustAccDepoistId")]/@value''').get()
        acc_number_vadiye = response.xpath(
            '''//*[(@id = "auctionDetailsViewAction-loadFormPart_auctionDto_auction_refundTrustAuctioneerAccount_description")]/@value''').get()
        paymentAccountsTxt = response.xpath('''//*[(@id = "paymentAccountsTxt")]/@value''').get()
        txtPaymentAccDepoistId = response.xpath('''//*[(@id = "txtPaymentAccDepoistId")]/@value''').get()
        acc_number_pay = response.xpath(
            '''//*[(@id = "auctionDetailsViewAction-loadFormPart_auctionDto_auction_refundAuctioneerAccount_description")]/@value''').get()

        I_data = {
            'id1': auc_num,
            'id2': aucTile,
            'id3': fromsiteshowdate,
            'id4': fss_time,
            'id5': tositeshowdate,
            'id6': tss_time,
            'id7': fromviewdate,
            'id8': toviewdate,
            'id9': fv_time,
            'id10': tv_time,
            'id11': rec_docDate,
            'id12': rec_doctime,
            'id13': fromproposaldate,
            'id14': fp_time,
            'id15': toproposaldate,
            'id16': tp_time,
            'id17': openingdate,
            'id18': op_time,
            'id19': winnerannouncedate,
            'id20': wa_time,
            'id21': pay_without,
            'id22': winner_ac,
            'id23': lastpaytime,
            'id24': penalty_pay,
            'id25': getwarehouse_without,
            'id26': getwarhouse,
            'id27': penalty_percent,
            'id28': days_exist,
            'id29': participationcost,
            'id30': receiptdocdate,
            'id31': rd_time,
            'id32': vadiye_percent,
            'id33': participateAccountsTxt,
            'id34': txtParticipateAccDepoistId,
            'id35': trustAccountsTxt,
            'id36': txtTrustAccDepoistId,
            'id37': acc_number_vadiye,
            'id38': paymentAccountsTxt,
            'id39': txtPaymentAccDepoistId,
            'id40': acc_number_pay
        }

        yield {"I_data": I_data}
