from django.template import Library
register = Library()

@register.inclusion_tag('rds/includes/package_actions.html')
def package_actions(package, farm):
    """
    Generates the actions for a package
    """
    farm_package = package.farm_packages.filter(farm=farm).first()
    return {
        'farm': farm,
        'package': package,
        'farm_package': farm_package
    }
