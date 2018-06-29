%module(directors="1") PyCTP

%begin %{
#define SWIG_PYTHON_STRICT_BYTE_CHAR
%}

%include "typemaps.i"

%{
#define SWIG_FILE_WITH_INIT

#include "./api/ThostFtdcMdApi.h"
#include "./api/ThostFtdcTraderApi.h"
#include "./api/ThostFtdcUserApiStruct.h"
#include "./api/ThostFtdcUserApiDataType.h"
%}

%ignore TThostFtdcVirementTradeCodeType;
%ignore THOST_FTDC_VTC_BankBankToFuture;
%ignore THOST_FTDC_VTC_BankFutureToBank;
%ignore THOST_FTDC_VTC_FutureBankToFuture;
%ignore THOST_FTDC_VTC_FutureFutureToBank;

%ignore TThostFtdcFBTTradeCodeEnumType;
%ignore THOST_FTDC_FTC_BankLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BrokerLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BankLaunchBrokerToBank;
%ignore THOST_FTDC_FTC_BrokerLaunchBrokerToBank;


%typemap(in) (char **ARRAY, int SIZE) {
    if (PyList_Check($input)) {
        int i = 0;
        $2 = PyList_Size($input);
        $1 = (char **)malloc(($2+1)*sizeof(char *));
        for (; i < $2; i++) {
            PyObject *o = PyList_GetItem($input,i);
            if (PyBytes_Check(o)) {
                $1[i] = PyBytes_AsString(PyList_GetItem($input,i));
            }
            else {
                free($1);
                PyErr_SetString(PyExc_TypeError,"list must contain bytes");
                SWIG_fail;
            }
        }
        $1[i] = 0;
    } else {
        PyErr_SetString(PyExc_TypeError, "not a list");
        SWIG_fail;
    }
}

%typemap(freearg) (char **ARRAY, int SIZE) {
    free((char *)$1);
}

%apply (char **ARRAY, int SIZE) { (char *ppInstrumentID[], int nCount) };


%feature("director") CThostFtdcMdSpi;
%include "./api/ThostFtdcMdApi.h"

%feature("director") CThostFtdcTraderSpi;
%include "./api/ThostFtdcTraderApi.h"

%include "./api/ThostFtdcUserApiDataType.h"
%include "./api/ThostFtdcUserApiStruct.h"
