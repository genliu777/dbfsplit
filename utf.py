import codecs
f = codecs.open('config.xml','w','utf-8')
txt = '''<?xml version="1.0" encoding="gb2312"?>
<DBFSplitter Author="Chinalions" Version="1.0">
	<!-- 支持的 CompType: COMP_EQUAL/COMP_NOTEQUAL/COMP_LESS/COMP_NOTLESS/COMP_GREAT/COMP_NOTGREAT, 即 = != < >= > <= -->
	<!-- 支持的 LinkType: AND/OR -->
	<!-- 日期通配符示例: 日期为2012年10月06日时, @Y@M@D = 20121006, @XM = A06; 日期为2012年3月10日时, @Y@M@D = 20120310, @XM = 310 -->
	<!-- 字段类型Type均填string, 程序内部所有类型转化为string后进行匹配 -->
	<!-- 同一<Filter>节点下的<Field>子节点以FieldID属性作为唯一主键 -->
	


  <!-- 中融-华林-光大-融华一号 需要的深交所数据
   深圳数据：Sjshb.dbf（回报库），Sjshq.dbf（行情库），Sjsgf.dbf（深交所股份库），Sjsdz.dbf（深交所对账库），LOFJS.dbf（LOF结算库）
       Sjsxx.dbf（深交所信息），Sjsfx.dbf（深交所发行），Sjsjg.dbf（深交所结果），Sjsmx1.dbf（深交所明细1），Sjsmx2.dbf（深交所明细2）。-->
  <DBFFile FileID="SJSHB_ZR" Description="深交所回报库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\sjshb\@Y@M@D\SJSHB.dbf"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSHB.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSHB.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="HBGDDM" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSHQ_ZR" Description="深交所行情库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\QSSJ\HQ\@Y@M@D\SJSHQ.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSHQ.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSHQ.DBF"/>
  	<Filter Description="分拆条件">
  		<!--Field FieldID="HQGDDM" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/-->
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSGF_ZR" Description="深交所股份结算信息库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\QSSJ\sjs\SJSGF.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSGF.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSGF.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="GFGDDM" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSDZ_ZR" Description="深交所股份结算对账库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\QSSJ\sjs\SJSDZ.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSDZ.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSDZ.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="DZGDDM" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSXX_ZR" Description="深交所证券信息库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\QSSJ\hq\@Y@M@D\SJSXX.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSXX.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSXX.DBF"/>
  	<Filter Description="分拆条件">
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSFX_ZR" Description="深交所发行信息库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\QSSJ\sjs\SJSFX.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSFX.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSFX.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="FXGDDM" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSTP_ZR" Description="深交所投票库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\QSSJ\sjs\SJSTP.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSTP.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSTP.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="HBGDDM" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>
  
 	<DBFFile FileID="SJSJG_ZR" Description="深交所结果库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\qssj\dcom\SJSJG.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSJG.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSJG.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="JGZQZH" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSMX1_ZR" Description="深交所明细库1">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\qssj\dcom\SJSMX1.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSMX1.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSMX1.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="MXZQZH" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>
  <DBFFile FileID="SJSMX2_ZR" Description="深交所明细库2">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\qssj\dcom\SJSMX2.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\SJSMX2.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\SJSMX2.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="MXZQZH" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>  
  
  <DBFFile FileID="LOFJS_ZR" Description="LOF结算库">
  	<Source      Description="源文件信息"      FileName="\\\\10.100.1.41\d$\QSSJ\sjs\LOFJS.DBF"/>
  	<Destination Description="中融信托"    SaveName="\\\\10.100.1.117\d$\send\T_ZHONGRONGGJ01\@Y@M@D\融华1号\LOFJS.DBF"/>
  	<Destination Description="光大银行"    SaveName="\\\\10.100.1.117\d$\send\k0247\光大银行\@Y@M@D\融华1号\LOFJS.DBF"/>
  	<Filter Description="分拆条件">
  		<Field FieldID="JSZQZH" FieldName="证券账户" FieldValue="0899044298" Type="string" CompType="COMP_EQUAL" LinkType="AND"/>
  	</Filter>
  </DBFFile>    
  
  
  
  
  
 
 
</DBFSplitter>
'''
# %s/\\\\/\\\\\\\\/
# %s/\\r/\\\\r/
f.write(txt)
f.close()
