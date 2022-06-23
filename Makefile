tfclean:
	rm -rf ./terraform .terraform && rm -rf terraform.lock.hcl && rm -rf terraform.tfstate && rm -rf terraform.tfstate.backup

aks-install-cli:
	az aks install-cli
	
aks-login:
	bash -c "az aks get-credentials --resource-group ${RESOURCE_GROUP_NAME} --name ${AKS_CLUSTER_NAME}"

test:
	source test/.venv/bin/activate && python ./test/test_aks.py

deploy:
	helm upgrade mymodel ./helm/mymodel --install --create-namespace --namespace mymodel
