PUB_STATUS_CHOICES = (
    ('D', 'Draft'),
    ('E', 'Edit'),
    ('P', 'Published'),
    ('T', 'Trash'),
)

PUB_STATUSES = dict((pair[1], pair[0]) for pair in PUB_STATUS_CHOICES)
