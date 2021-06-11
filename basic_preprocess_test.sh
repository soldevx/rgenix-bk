#!/bin/bash
IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=resgenix_bk_container"))
echo "Found IP ${IP}"
echo ""
echo "============================== Test [Add Meta User] ==============================="
echo ""
curl -X GET http://${IP}:5000/api/users
echo ""
echo ""
echo "===================== Test [Preprocess & Add Job Description] ====================="
echo ""
curl -sS -F file=@"basic_test/job_desc/jobdesc.pdf" -X POST "http://${IP}:5000/api/preprocess?uid=1&type=jobdesc"
echo ""
echo ""
echo "=========================== Test [Preprocess & Add CV] ============================"
echo ""
curl -sS -F file=@"basic_test/appliants/8Holly.pdf" -X POST "http://${IP}:5000/api/preprocess?uid=1&type=cv&&jid=1"
echo ""
echo ""
echo "==================================================================================="s
