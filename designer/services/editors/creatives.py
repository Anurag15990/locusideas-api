__author__ = 'anurag'

from designer.services.editors.base import BaseEditor, response_handler
from designer.models.creatives import PortFolio, Designs

class CreativesEditor(BaseEditor):

        def _invoke(self):
            if self.command == 'create-new-portfolio':
                response = create_new_portfolio(self.data)
            elif self.command == 'update-portfolio':
                response = update_portfolio(self.node, self.data)
            elif self.command == 'update-category':
                response = update_category(self.action, self.node, self.data['category'])
            elif self.command == 'update-sub-category':
                response = update_sub_category(self.action, self.node, self.data['subcategory'])
            elif self.command == 'update-view-count':
                response = update_view_count(self.node, self.data)
            elif self.command == 'update-tags':
                response = update_tags(self.action, self.node, self.data['tags'])
            return response

@response_handler('Portfolio created successfully', 'Error occurred while creating Portfolio', login_required=True)
def create_new_portfolio(data):
    portfolio = PortFolio.create(title=data['title'], owner=data['owner'])
    if data['description'] is not None:
        portfolio.description = data['description']

    if data['category'] is not None:
        portfolio.category = data['category']

    if data['sub-category'] is not None:
        portfolio.sub_category = data['sub-category']

    if data['tags'] is not None:
        portfolio.tags = data['tags']

    portfolio.save()
    return portfolio

@response_handler('Portfolio updated successfully', 'Failed to update Portfolio', login_required=True)
def update_portfolio(portfolio,data):
    node = portfolio.objects(pk=portfolio).first()

    if data['title'] is not None:
        portfolio.title = data['title']

    if data['description'] is not None:
        portfolio.description = data['description']

    node.save()
    return node

@response_handler('Category updated successfully', 'Failed to update Category', login_required=True)
def update_category(action, portfolio, category):
    node = portfolio.objects(pk=portfolio).first()

    if action == "add":
        node.category.append(category)
    elif action == "remove":
        node.category.remove(category)

    node.save()
    return node

@response_handler('Sub-category updated successfully', 'Failed to update Sub-category', login_required=True)
def update_sub_category(action, portfolio, sub_category):
    node = portfolio.objects(pk=portfolio).first()

    if action == "add":
        node.sub_category.append(sub_category)
    elif action == "remove":
        node.sub_category.remove(sub_category)

    node.save()
    return node

@response_handler('Tags updated successfully', 'Failed to update Tags', login_required=True)
def update_tags(action, portfolio, tag):
    node = portfolio.objects(pk=portfolio).first()

    if action == "add":
        node.tags.append(tag)
    elif action == "remove":
        node.tags.remove(tag)

    node.save()
    return node

def update_view_count(portfolio, data):
    node = portfolio.objects(pk=portfolio).first()

    pass


