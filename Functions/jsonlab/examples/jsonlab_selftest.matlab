
                            < M A T L A B (R) >
                  Copyright 1984-2010 The MathWorks, Inc.
                Version 7.11.0.584 (R2010b) 64-bit (glnxa64)
                              August 16, 2010

 
  To get started, type one of these: helpwin, helpdesk, or demo.
  For product information, visit www.mathworks.com.
 
>> >> >> >> >> ===============================================
>> example1.json
{
	"data": {
		"firstName": "John",
		"lastName": "Smith",
		"age": 25,
		"address": {
			"streetAddress": "21 2nd Street",
			"city": "New York",
			"state": "NY",
			"postalCode": "10021"
		},
		"phoneNumber": [
			{
				"type": "home",
				"number": "212 555-1234"
			},
			{
				"type": "fax",
				"number": "646 555-4567"
			}
		]
	}
}

{"data": {"firstName": "John","lastName": "Smith","age": 25,"address": {"streetAddress": "21 2nd Street","city": "New York","state": "NY","postalCode": "10021"},"phoneNumber": [{"type": "home","number": "212 555-1234"},{"type": "fax","number": "646 555-4567"}]}}

===============================================
>> example2.json
{
	"data": {
		"glossary": {
			"title": "example glossary",
			"GlossDiv": {
				"title": "S",
				"GlossList": {
					"GlossEntry": {
						"ID": "SGML",
						"SortAs": "SGML",
						"GlossTerm": "Standard Generalized Markup Language",
						"Acronym": "SGML",
						"Abbrev": "ISO 8879:1986",
						"GlossDef": {
							"para": "A meta-markup language, used to create markup languages such as DocBook.",
							"GlossSeeAlso": [
								"GML",
								"XML"
							]
						},
						"GlossSee": "markup"
					}
				}
			}
		}
	}
}

{"data": {"glossary": {"title": "example glossary","GlossDiv": {"title": "S","GlossList": {"GlossEntry": {"ID": "SGML","SortAs": "SGML","GlossTerm": "Standard Generalized Markup Language","Acronym": "SGML","Abbrev": "ISO 8879:1986","GlossDef": {"para": "A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso": ["GML","XML"]},"GlossSee": "markup"}}}}}}

===============================================
>> example3.json
{
	"data": {
		"menu": {
			"id": "file",
			"value": "_&File",
			"popup": {
				"menuitem": [
					{
						"value": "_&New",
						"onclick": "CreateNewDoc(\"'\\\"Untitled\\\"'\")"
					},
					{
						"value": "_&Open",
						"onclick": "OpenDoc()"
					},
					{
						"value": "_&Close",
						"onclick": "CloseDoc()"
					}
				]
			}
		}
	}
}

{"data": {"menu": {"id": "file","value": "_&File","popup": {"menuitem": [{"value": "_&New","onclick": "CreateNewDoc(\"'\\\"Untitled\\\"'\")"},{"value": "_&Open","onclick": "OpenDoc()"},{"value": "_&Close","onclick": "CloseDoc()"}]}}}}

===============================================
>> example4.json
{
	"data": [
		{
			"sample": {
				"rho": 1
			}
		},
		{
			"sample": {
				"rho": 2
			}
		},
		[
			[1,0],
			[1,1],
			[1,2]
		],
		[
			"Paper",
			"Scissors",
			"Stone"
		],
		[
			"a",
			"b\\",
			"c\"",
			"d\\\"",
			"e\"[",
			"f\\\"[",
			"g[\\",
			"h[\\\""
		]
	]
}

{"data": [{"sample": {"rho": 1}},{"sample": {"rho": 2}},[[1,0],[1,1],[1,2]],["Paper","Scissors","Stone"],["a","b\\","c\"","d\\\"","e\"[","f\\\"[","g[\\","h[\\\""]]}

>> >> ===============================================
>> example1.json
{Udata{U	firstNameSUJohnUlastNameSUSmithUageiUaddress{UstreetAddressSU21 2nd StreetUcitySUNew YorkUstateSUNYU
postalCodeSU10021}UphoneNumber[{UtypeSUhomeUnumberSU212 555-1234}{UtypeSUfaxUnumberSU646 555-4567}]}}
===============================================
>> example2.json
{Udata{Uglossary{UtitleSUexample glossaryUGlossDiv{UtitleCSU	GlossList{U
GlossEntry{UIDSUSGMLUSortAsSUSGMLU	GlossTermSU$Standard Generalized Markup LanguageUAcronymSUSGMLUAbbrevSUISO 8879:1986UGlossDef{UparaSUHA meta-markup language, used to create markup languages such as DocBook.UGlossSeeAlso[SUGMLSUXML]}UGlossSeeSUmarkup}}}}}}
===============================================
>> example3.json
{Udata{Umenu{UidSUfileUvalueSU_&FileUpopup{Umenuitem[{UvalueSU_&NewUonclickSUCreateNewDoc("'\"Untitled\"'")}{UvalueSU_&OpenUonclickSU	OpenDoc()}{UvalueSU_&CloseUonclickSU
CloseDoc()}]}}}}
===============================================
>> example4.json
{Udata[{Usample{Urhoi}}{Usample{Urhoi}}[[$i#U[$i#U[$i#U][SUPaperSUScissorsSUStone][CaSUb\SUc"SUd\"SUe"[SUf\"[SUg[\SUh[\"]]}
>> 