/* soapServiceSoapBindingProxy.h
   Generated by gSOAP 2.8.12 from service.1cws?wsdl.h

Copyright(C) 2000-2012, Robert van Engelen, Genivia Inc. All Rights Reserved.
The generated code is released under one of the following licenses:
1) GPL or 2) Genivia's license for commercial use.
This program is released under the GPL with the additional exemption that
compiling, linking, and/or using OpenSSL is allowed.
*/

#ifndef soapServiceSoapBindingProxy_H
#define soapServiceSoapBindingProxy_H
#include "soapH.h"

class SOAP_CMAC ServiceSoapBindingProxy : public soap
{ public:
	/// Endpoint URL of service 'ServiceSoapBindingProxy' (change as needed)
	const char *soap_endpoint;
	/// Constructor
	ServiceSoapBindingProxy();
	/// Construct from another engine state
	ServiceSoapBindingProxy(const struct soap&);
	/// Constructor with endpoint URL
	ServiceSoapBindingProxy(const char *url);
	/// Constructor with engine input+output mode control
	ServiceSoapBindingProxy(soap_mode iomode);
	/// Constructor with URL and input+output mode control
	ServiceSoapBindingProxy(const char *url, soap_mode iomode);
	/// Constructor with engine input and output mode control
	ServiceSoapBindingProxy(soap_mode imode, soap_mode omode);
	/// Destructor frees deserialized data
	virtual	~ServiceSoapBindingProxy();
	/// Initializer used by constructors
	virtual	void ServiceSoapBindingProxy_init(soap_mode imode, soap_mode omode);
	/// Delete all deserialized data (uses soap_destroy and soap_end)
	virtual	void destroy();
	/// Delete all deserialized data and reset to default
	virtual	void reset();
	/// Disables and removes SOAP Header from message
	virtual	void soap_noheader();
	/// Get SOAP Header structure (NULL when absent)
	virtual	const SOAP_ENV__Header *soap_header();
	/// Get SOAP Fault structure (NULL when absent)
	virtual	const SOAP_ENV__Fault *soap_fault();
	/// Get SOAP Fault string (NULL when absent)
	virtual	const char *soap_fault_string();
	/// Get SOAP Fault detail as string (NULL when absent)
	virtual	const char *soap_fault_detail();
	/// Close connection (normally automatic, except for send_X ops)
	virtual	int soap_close_socket();
	/// Force close connection (can kill a thread blocked on IO)
	virtual	int soap_force_close_socket();
	/// Print fault
	virtual	void soap_print_fault(FILE*);
#ifndef WITH_LEAN
	/// Print fault to stream
#ifndef WITH_COMPAT
	virtual	void soap_stream_fault(std::ostream&);
#endif

	/// Put fault into buffer
	virtual	char *soap_sprint_fault(char *buf, size_t len);
#endif

	/// Web service operation 'getName' (returns error code or SOAP_OK)
	virtual	int getName(_ns1__getName *ns1__getName, _ns1__getNameResponse *ns1__getNameResponse) { return this->getName(NULL, NULL, ns1__getName, ns1__getNameResponse); }
	virtual	int getName(const char *endpoint, const char *soap_action, _ns1__getName *ns1__getName, _ns1__getNameResponse *ns1__getNameResponse);

	/// Web service operation 'runCode' (returns error code or SOAP_OK)
	virtual	int runCode(_ns1__runCode *ns1__runCode, _ns1__runCodeResponse *ns1__runCodeResponse) { return this->runCode(NULL, NULL, ns1__runCode, ns1__runCodeResponse); }
	virtual	int runCode(const char *endpoint, const char *soap_action, _ns1__runCode *ns1__runCode, _ns1__runCodeResponse *ns1__runCodeResponse);

	/// Web service operation 'Start' (returns error code or SOAP_OK)
	virtual	int Start(_ns1__Start *ns1__Start, _ns1__StartResponse *ns1__StartResponse) { return this->Start(NULL, NULL, ns1__Start, ns1__StartResponse); }
	virtual	int Start(const char *endpoint, const char *soap_action, _ns1__Start *ns1__Start, _ns1__StartResponse *ns1__StartResponse);

	/// Web service operation 'Status' (returns error code or SOAP_OK)
	virtual	int Status(_ns1__Status *ns1__Status, _ns1__StatusResponse *ns1__StatusResponse) { return this->Status(NULL, NULL, ns1__Status, ns1__StatusResponse); }
	virtual	int Status(const char *endpoint, const char *soap_action, _ns1__Status *ns1__Status, _ns1__StatusResponse *ns1__StatusResponse);

	/// Web service operation 'Stop' (returns error code or SOAP_OK)
	virtual	int Stop(_ns1__Stop *ns1__Stop, _ns1__StopResponse *ns1__StopResponse) { return this->Stop(NULL, NULL, ns1__Stop, ns1__StopResponse); }
	virtual	int Stop(const char *endpoint, const char *soap_action, _ns1__Stop *ns1__Stop, _ns1__StopResponse *ns1__StopResponse);

	/// Web service operation 'getName' (returns error code or SOAP_OK)
	virtual	int getName_(_ns1__getName *ns1__getName, _ns1__getNameResponse *ns1__getNameResponse) { return this->getName_(NULL, NULL, ns1__getName, ns1__getNameResponse); }
	virtual	int getName_(const char *endpoint, const char *soap_action, _ns1__getName *ns1__getName, _ns1__getNameResponse *ns1__getNameResponse);

	/// Web service operation 'runCode' (returns error code or SOAP_OK)
	virtual	int runCode_(_ns1__runCode *ns1__runCode, _ns1__runCodeResponse *ns1__runCodeResponse) { return this->runCode_(NULL, NULL, ns1__runCode, ns1__runCodeResponse); }
	virtual	int runCode_(const char *endpoint, const char *soap_action, _ns1__runCode *ns1__runCode, _ns1__runCodeResponse *ns1__runCodeResponse);

	/// Web service operation 'Start' (returns error code or SOAP_OK)
	virtual	int Start_(_ns1__Start *ns1__Start, _ns1__StartResponse *ns1__StartResponse) { return this->Start_(NULL, NULL, ns1__Start, ns1__StartResponse); }
	virtual	int Start_(const char *endpoint, const char *soap_action, _ns1__Start *ns1__Start, _ns1__StartResponse *ns1__StartResponse);

	/// Web service operation 'Status' (returns error code or SOAP_OK)
	virtual	int Status_(_ns1__Status *ns1__Status, _ns1__StatusResponse *ns1__StatusResponse) { return this->Status_(NULL, NULL, ns1__Status, ns1__StatusResponse); }
	virtual	int Status_(const char *endpoint, const char *soap_action, _ns1__Status *ns1__Status, _ns1__StatusResponse *ns1__StatusResponse);

	/// Web service operation 'Stop' (returns error code or SOAP_OK)
	virtual	int Stop_(_ns1__Stop *ns1__Stop, _ns1__StopResponse *ns1__StopResponse) { return this->Stop_(NULL, NULL, ns1__Stop, ns1__StopResponse); }
	virtual	int Stop_(const char *endpoint, const char *soap_action, _ns1__Stop *ns1__Stop, _ns1__StopResponse *ns1__StopResponse);
};
#endif
