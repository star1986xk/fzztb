headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Content-Type': 'application/json'
}

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
}

# # # 福州市 # # #
# 福州市工程 索引页 URL
fzztb_project_index_url = '/CmsPortalWeb/CmsMainData/tenderInfo.xhtml?small=0'
# 福州市工程 索引页 参数
fzztb_project_index_data = {"page": {"pageSize": 10, "currentPage": 1}, "modelObj": {},
                            "queryCondition": {"tmBidSectionQueryObj": {"modelObj": {"categoryId": "10001010101"}},
                                               "needQueryJoin__tmBidSectionQueryObj": True},
                            "orderByStr": " update_time desc"}
# 福州市工程 项目页 url
fzztb_project_url = '/CmsPortalWeb/main/queryProcess.xhtml?secId={}&proId=3003&seqId=null'
# 福州市工程 pdfsn url
fzztb_pdf_sn_url = '/CmsPortalWeb/CmsProcessData/getTenderObjBySecId.xhtml'
# 福州市工程 zbfsn url
fzztb_zbf_sn_url = '/CmsPortalWeb/CmsProcessData/getDocumentsObjBySecId.xhtml'
# 福州市工程 下载页 url
fzztb_down_url = '/BaseSystemMgrWeb/ebidfile/getFileBySn/{}.xhtml'


# 福州市保证金 索引页 URL
fzztb_recognizance_index_url = '/CmsPortalWeb/ztbServiceData/recognizancePageCountByArgs.xhtml'
# 福州市保证金 索引页 参数
fzztb_recognizance_index_data = {"page": {"pageSize": 10, "currentPage": 1}, "modelObj": {"isDel": 1},
                                 "queryCondition": {}, "orderByStr": "  create_time desc"}
# 福州市保证金 保证金页 URL
fzztb_recognizance_url = '/CmsPortalWeb/ztbServiceData/recognizanceQueryByArgs.xhtml'
# 福州市保证金 保证金页 参数
fzztb_recognizance_data = {"modelObj": {"isDel": 1, "sectionName": None, "remark3": "1"},
                           "orderByStr": "  create_time asc"}
# 数据库存储url
fzztb_recognizance = '/CmsPortalWeb/main/service.xhtml'


# # # 龙岩市 # # #
# 龙岩市工程 索引页 URL
lyggzy_project_index_url = '/lyztb/gcjs/081001/081001003/08100100300{}/?pageing={}'


# 龙岩市保证金 索引页 URL
lyggzy_recognizance_index_url = '/lyhy/ZHManageMis_LY/Pages/WebList/TB_T_List.aspx'
# 龙岩市保证金 单位 URL
lyggzy_recognizance_company_url = '/lyhy/ZHManageMis_LY/Pages/WebList/DanWei_List.aspx?tg={}'
# 数据库存储url
lyggzy_recognizance = '/lyztb/ndbzj/089005/'


# 保证金对象
recognizance = {
    'siteName': None,
    'domain': None,
    'projectId': None,
    'projectName': None,
    'projectNumber': None,
    'projectUrl': None,
    'company': None,
}

# 工程对象
project = {
    'siteName': None,
    'domain': None,
    'projectId': None,
    'projectName': None,
    'projectNumber': None,
    'projectUrl': None,
    'annexUrl': None,
}
