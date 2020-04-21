from post_scene.post_scene import PostScene

yaml_path = './yaml/demo.yaml'  # 脚本文件的路径
xmind_path = './xmind/demo.xmind'  # 脚本文件的路径
api_document_path = './api_document/demo.postman_collection.json'  # postman json data 文件的路径
api_document_url = 'https://www.getpostman.com/collections/08ab1192c204d8df4a48'  # 也可以使用Postman的share link


# PostScene.covert(yaml_path, api_document_path,scene_dirs='./scene')
# PostScene.covert(xmind_path, api_document_path,scene_dirs='./scene')
PostScene.covert(yaml_path, api_document_url,scene_dirs='./scene')


