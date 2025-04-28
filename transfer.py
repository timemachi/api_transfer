import json
import os
import argparse

def modify_openapi_for_aws(file_name):
    # 读取原始JSON文件
    with open(f"data/{file_name}", 'r', encoding='utf-8') as file:
        openapi_data = json.load(file)

    # 遍历所有路径并添加AWS API Gateway集成配置
    for path, methods in openapi_data.get('paths', {}).items():
        for method, details in methods.items():
            # 添加x-amazon-apigateway-integration配置
            details['x-amazon-apigateway-integration'] = {
                "payloadFormatVersion": "1.0",
                "type": "http_proxy",
                "httpMethod": method.upper(),
                "uri": f"http://${{stageVariables.backendUrl}}{path}",
                "connectionType": "INTERNET"
            }

    # 生成新的文件名
    base_name, ext = os.path.splitext(file_name)
    new_file_name = f"{base_name}_modified{ext}"

    # 将修改后的数据写入新的JSON文件
    with open(f"data/{new_file_name}", 'w', encoding='utf-8') as file:
        json.dump(openapi_data, file, indent=2, ensure_ascii=False)

    print(f"Modified OpenAPI file saved as: data/{new_file_name}")

# 使用示例
def main():
    parser = argparse.ArgumentParser(description='Modify OpenAPI JSON for AWS API Gateway.')
    parser.add_argument('file_name', type=str, help='The name of the JSON file to modify')
    args = parser.parse_args()

    modify_openapi_for_aws(args.file_name)

if __name__ == "__main__":
    main()
# python .\transfer.py api-docs-20250321.json