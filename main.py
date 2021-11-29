from website import create_app 
from website.api import UserAPI, CollectionAPI, CardAPI

(app,api) = create_app()
api.add_resource(UserAPI,"/api/user" , "/api/user/<int:id>")
api.add_resource(CollectionAPI,"/api/collection" , "/api/user/<int:id>")
api.add_resource(CardAPI,"/api/card" , "/api/card/<int:id>")

if __name__ == '__main__':
    app.run(debug = True)
