def publication():
    """
    Returns a tuple for adding a Publication Information section to an admin.
    """
    return ('Publication Information', {
        'fields': ('pub_date', 'pub_status', 'sites', ),
    })

def authors():
    """
    Returns a tuple for adding an Authors Information section to an admin.
    """
    return ('Author Information', {
        'fields': ('authors', 'authors_override', 'authors_extra'),
    })
