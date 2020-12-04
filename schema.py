import graphene
import json
from datetime import datetime
import uuid
class Post(graphene.ObjectType):
  title = graphene.String()
  content = graphene.String()



class User(graphene.ObjectType):
  id = graphene.ID(default_value=str(uuid.uuid4()))
  username = graphene.String()
  created_at = graphene.DateTime(default_value=datetime.now())
  #how to use self
  avatar_url = graphene.String()
  def resolve_avatar_url(self,info):
    return "http://cloudinary.com/{}/{}".format(self.username,self.id)


class Query(graphene.ObjectType):
  users = graphene.List(User, limit = graphene.Int())
  hello = graphene.String() #field and datatype
  is_admin = graphene.Boolean()

  #resolveOperation,in snake case
  def resolve_hello(self, info):
    return "world"
  def resolve_is_admin(self, info):
    return True
  def resolve_users(self,info,limit=None):
    return [
      User(id = "1",username = "Fred", created_at = datetime.now()),
      User(id = "2",username = "Fred2", created_at = datetime.now()),
      User(id = "3",username = "Fred3", created_at = datetime.now()),
    ][:limit]
class CreateUser(graphene.Mutation):
  user = graphene.Field(User)

  class Arguments:
    username = graphene.String()
  #name will always be mutate for every mutation  
  def mutate(self, info, username):
    user = User(username = username)
    return CreateUser(user = user)


class CreatePost(graphene.Mutation):
  post = graphene.Field(Post)

  class Arguments:
    title = graphene.String()
    content = graphene.String()

  def mutate(self, info, title,content):
    #info and context
    if info.context.get('is_anonymous'):
      raise Exception('Not authenticated!')
    post = Post(title = title,content = content)
    return CreatePost(post = post)



class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  create_post = CreatePost.Field()



schema = graphene.Schema(query=Query, mutation = Mutation)

result = schema.execute(
  #must be in camel case
  #or set when creating schema: auto_camelcase = False
  #!means is required
    '''
    {
      users{
        id
        createdAt
        username
        avatarUrl
      }
    }
    ''',
    #variable_values = {'limit':2}
    # context = {'is_anonymous':True}
    )
dictResult = dict(result.data.items())
print (json.dumps(dictResult,indent = 2))
