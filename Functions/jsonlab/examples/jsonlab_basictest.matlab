
                            < M A T L A B (R) >
                  Copyright 1984-2010 The MathWorks, Inc.
                Version 7.11.0.584 (R2010b) 64-bit (glnxa64)
                              August 16, 2010

 
  To get started, type one of these: helpwin, helpdesk, or demo.
  For product information, visit www.mathworks.com.
 
>> >> >> >> >> >> >> >> >> 
%=================================================
>> %  a simple scalar value 
>> %=================================================

>> >> 
data2json =

    3.1416

>> 
ans =

[3.141592654]


>> 
json2data =

    3.1416

>> >> 
%=================================================
>> %  a complex number
>> %=================================================

>> >> >> 
data2json =

   1.0000 + 2.0000i

>> 
ans =

{
	"_ArrayType_": "double",
	"_ArraySize_": [1,1],
	"_ArrayIsComplex_": 1,
	"_ArrayData_": [1,2]
}


>> 
json2data =

   1.0000 + 2.0000i

>> >> 
%=================================================
>> %  a complex matrix
>> %=================================================

>> >> >> 
data2json =

  35.0000 +26.0000i   1.0000 +19.0000i   6.0000 +24.0000i
   3.0000 +21.0000i  32.0000 +23.0000i   7.0000 +25.0000i
  31.0000 +22.0000i   9.0000 +27.0000i   2.0000 +20.0000i
   8.0000 +17.0000i  28.0000 +10.0000i  33.0000 +15.0000i
  30.0000 +12.0000i   5.0000 +14.0000i  34.0000 +16.0000i
   4.0000 +13.0000i  36.0000 +18.0000i  29.0000 +11.0000i

>> 
ans =

{
	"_ArrayType_": "double",
	"_ArraySize_": [6,3],
	"_ArrayIsComplex_": 1,
	"_ArrayData_": [
		[35,26],
		[3,21],
		[31,22],
		[8,17],
		[30,12],
		[4,13],
		[1,19],
		[32,23],
		[9,27],
		[28,10],
		[5,14],
		[36,18],
		[6,24],
		[7,25],
		[2,20],
		[33,15],
		[34,16],
		[29,11]
	]
}


>> 
json2data =

  35.0000 +26.0000i   1.0000 +19.0000i   6.0000 +24.0000i
   3.0000 +21.0000i  32.0000 +23.0000i   7.0000 +25.0000i
  31.0000 +22.0000i   9.0000 +27.0000i   2.0000 +20.0000i
   8.0000 +17.0000i  28.0000 +10.0000i  33.0000 +15.0000i
  30.0000 +12.0000i   5.0000 +14.0000i  34.0000 +16.0000i
   4.0000 +13.0000i  36.0000 +18.0000i  29.0000 +11.0000i

>> >> 
%=================================================
>> %  MATLAB special constants
>> %=================================================

>> >> 
data2json =

   NaN   Inf  -Inf

>> 
ans =

{
	"specials": ["_NaN_","_Inf_","-_Inf_"]
}


>> 
json2data = 

    specials: [NaN Inf -Inf]

>> >> 
%=================================================
>> %  a real sparse matrix
>> %=================================================

>> >> 
data2json =

   (1,2)       0.6557
   (9,2)       0.7577
   (3,5)       0.8491
  (10,5)       0.7431
  (10,8)       0.3922
   (7,9)       0.6787
   (2,10)      0.0357
   (6,10)      0.9340
  (10,10)      0.6555

>> 
ans =

{
	"sparse": {
		"_ArrayType_": "double",
		"_ArraySize_": [10,10],
		"_ArrayIsSparse_": 1,
		"_ArrayData_": [
			[1,2,0.6557406992],
			[9,2,0.7577401306],
			[3,5,0.8491293059],
			[10,5,0.7431324681],
			[10,8,0.3922270195],
			[7,9,0.6787351549],
			[2,10,0.03571167857],
			[6,10,0.9339932478],
			[10,10,0.6554778902]
		]
	}
}


>> 
json2data = 

    sparse: [10x10 double]

>> >> 
%=================================================
>> %  a complex sparse matrix
>> %=================================================

>> >> 
data2json =

   (1,2)      0.6557 - 0.6557i
   (9,2)      0.7577 - 0.7577i
   (3,5)      0.8491 - 0.8491i
  (10,5)      0.7431 - 0.7431i
  (10,8)      0.3922 - 0.3922i
   (7,9)      0.6787 - 0.6787i
   (2,10)     0.0357 - 0.0357i
   (6,10)     0.9340 - 0.9340i
  (10,10)     0.6555 - 0.6555i

>> 
ans =

{
	"complex_sparse": {
		"_ArrayType_": "double",
		"_ArraySize_": [10,10],
		"_ArrayIsComplex_": 1,
		"_ArrayIsSparse_": 1,
		"_ArrayData_": [
			[1,2,0.6557406992,-0.6557406992],
			[9,2,0.7577401306,-0.7577401306],
			[3,5,0.8491293059,-0.8491293059],
			[10,5,0.7431324681,-0.7431324681],
			[10,8,0.3922270195,-0.3922270195],
			[7,9,0.6787351549,-0.6787351549],
			[2,10,0.03571167857,-0.03571167857],
			[6,10,0.9339932478,-0.9339932478],
			[10,10,0.6554778902,-0.6554778902]
		]
	}
}


>> 
json2data = 

    complex_sparse: [10x10 double]

>> >> 
%=================================================
>> %  an all-zero sparse matrix
>> %=================================================

>> >> >> 
ans =

{
	"all_zero_sparse": {
		"_ArrayType_": "double",
		"_ArraySize_": [2,3],
		"_ArrayIsSparse_": 1,
		"_ArrayData_": null
	}
}


>> 
json2data = 

    all_zero_sparse: [2x3 double]

>> >> 
%=================================================
>> %  an empty sparse matrix
>> %=================================================

>> >> >> 
ans =

{
	"empty_sparse": {
		"_ArrayType_": "double",
		"_ArraySize_": [0,0],
		"_ArrayIsSparse_": 1,
		"_ArrayData_": null
	}
}


>> 
json2data = 

    empty_sparse: []

>> >> 
%=================================================
>> %  an empty 0-by-0 real matrix
>> %=================================================

>> >> >> 
ans =

{
	"empty_0by0_real": null
}


>> 
json2data = 

    empty_0by0_real: []

>> >> 
%=================================================
>> %  an empty 0-by-3 real matrix
>> %=================================================

>> >> >> 
ans =

{
	"empty_0by3_real": {
		"_ArrayType_": "double",
		"_ArraySize_": [0,3],
		"_ArrayData_": null
	}
}


>> 
json2data = 

    empty_0by3_real: [0x3 double]

>> >> 
%=================================================
>> %  a sparse real column vector
>> %=================================================

>> >> >> 
ans =

{
	"sparse_column_vector": {
		"_ArrayType_": "double",
		"_ArraySize_": [5,1],
		"_ArrayIsSparse_": 1,
		"_ArrayData_": [
			[2,3],
			[4,1],
			[5,4]
		]
	}
}


>> 
json2data = 

    sparse_column_vector: [5x1 double]

>> >> 
%=================================================
>> %  a sparse complex column vector
>> %=================================================

>> >> >> 
ans =

{
	"complex_sparse_column_vector": {
		"_ArrayType_": "double",
		"_ArraySize_": [5,1],
		"_ArrayIsComplex_": 1,
		"_ArrayIsSparse_": 1,
		"_ArrayData_": [
			[2,3,-3],
			[4,1,-1],
			[5,4,-4]
		]
	}
}


>> 
json2data = 

    complex_sparse_column_vector: [5x1 double]

>> >> 
%=================================================
>> %  a sparse real row vector
>> %=================================================

>> >> >> 
ans =

{
	"sparse_row_vector": {
		"_ArrayType_": "double",
		"_ArraySize_": [1,5],
		"_ArrayIsSparse_": 1,
		"_ArrayData_": [
			[2,3],
			[4,1],
			[5,4]
		]
	}
}


>> 
json2data = 

    sparse_row_vector: [0 3 0 1 4]

>> >> 
%=================================================
>> %  a sparse complex row vector
>> %=================================================

>> >> >> 
ans =

{
	"complex_sparse_row_vector": {
		"_ArrayType_": "double",
		"_ArraySize_": [1,5],
		"_ArrayIsComplex_": 1,
		"_ArrayIsSparse_": 1,
		"_ArrayData_": [
			[2,3,-3],
			[4,1,-1],
			[5,4,-4]
		]
	}
}


>> 
json2data = 

    complex_sparse_row_vector: [1x5 double]

>> >> 
%=================================================
>> %  a structure
>> %=================================================

>> >> 
data2json = 

        name: 'Think Different'
        year: 1997
       magic: [3x3 double]
     misfits: [Inf NaN]
    embedded: [1x1 struct]

>> 
ans =

{
	"astruct": {
		"name": "Think Different",
		"year": 1997,
		"magic": [
			[8,1,6],
			[3,5,7],
			[4,9,2]
		],
		"misfits": ["_Inf_","_NaN_"],
		"embedded": {
			"left": true,
			"right": false
		}
	}
}


>> 
json2data = 

    astruct: [1x1 struct]

>> 
ans =

logical

>> >> 
%=================================================
>> %  a structure array
>> %=================================================

>> >> >> >> >> 
ans =

{
	"Supreme Commander": [
		{
			"name": "Nexus Prime",
			"rank": 9
		},
		{
			"name": "Sentinel Prime",
			"rank": 9
		},
		{
			"name": "Optimus Prime",
			"rank": 9
		}
	]
}


>> 
json2data = 

    Supreme_0x20_Commander: {[1x1 struct]  [1x1 struct]  [1x1 struct]}

>> >> 
%=================================================
>> %  a cell array
>> %=================================================

>> >> >> >> >> 
data2json = 

    [1x1 struct]
    [1x1 struct]
    [1x4 double]

>> 
ans =

{
	"debian": [
		[
			{
				"buzz": 1.10,
				"rex": 1.20,
				"bo": 1.30,
				"hamm": 2.00,
				"slink": 2.10,
				"potato": 2.20,
				"woody": 3.00,
				"sarge": 3.10,
				"etch": 4.00,
				"lenny": 5.00,
				"squeeze": 6.00,
				"wheezy": 7.00
			}
		],
		[
			{
				"Ubuntu": [
					"Kubuntu",
					"Xubuntu",
					"Lubuntu"
				]
			}
		],
		[
			[10.04,10.10,11.04,11.10]
		]
	]
}


>> 
json2data = 

    debian: {{1x1 cell}  {1x1 cell}  [10.0400 10.1000 11.0400 11.1000]}

>> >> 
%=================================================
>> %  invalid field-name handling
>> %=================================================

>> >> 
json2data = 

               ValidName: 1
       x0x5F_InvalidName: 2
       x0x3A_Field_0x3A_: 3
    x0xE9A1B9__0xE79BAE_: '绝密'

>> >> 
%=================================================
>> %  a 2D cell array
>> %=================================================

>> >> >> 
ans =

{
	"data2json": [
		[
			[
				1,
				[
					2,
					3
				]
			],
			[
				4,
				5
			],
			[
				6
			]
		],
		[
			[
				7
			],
			[
				8,
				9
			],
			[
				10
			]
		]
	]
}


>> 
json2data = 

    data2json: {{1x3 cell}  {1x3 cell}}

>> >> 
%=================================================
>> %  a 2D struct array
>> %=================================================

>> >> 
data2json = 

2x3 struct array with fields:
    idx
    data

>> >> 
ans =

{
	"data2json": [
		[
			{
				"idx": 1,
				"data": "structs"
			},
			{
				"idx": 2,
				"data": "structs"
			}
		],
		[
			{
				"idx": 3,
				"data": "structs"
			},
			{
				"idx": 4,
				"data": "structs"
			}
		],
		[
			{
				"idx": 5,
				"data": "structs"
			},
			{
				"idx": 6,
				"data": "structs"
			}
		]
	]
}


>> 
json2data = 

    data2json: {{1x2 cell}  {1x2 cell}  {1x2 cell}}

>> >> >> >> 