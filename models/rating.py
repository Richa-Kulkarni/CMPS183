# coding: utf8
from plugin_rating_widget import RatingWidget
db.define_table('product',
    Field('rating', 'integer',
          requires=IS_IN_SET(range(1,6)), # "requires" is necessary for the rating widget
))
################################ The core ######################################
# Inject the horizontal radio widget
db.product.rating.widget = RatingWidget()
################################################################################
