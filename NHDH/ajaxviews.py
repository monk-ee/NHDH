import flask_sijax
from NHDH import app

flask_sijax.Sijax(app)


@flask_sijax.route(app, '/report/<filename>')
def owner(filename):
    # Every Sijax handler function (like this one) receives at least
    # one parameter automatically, much like Python passes `self`
    # to object methods.
    # The `obj_response` parameter is the function's way of talking
    # back to the browser
    def t3(obj_response, t3):
        days = day_by_itemdescription(t3, filename)
        obj_response.alert('Days are %s' % (days))
        #obj_response.html_append('#'+t3, '<li>%s</li>' % (days))

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('t3', t3)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    mdf = month_by_itemdescription(filename)
    return render_template('breakdown.html',
                           mdf=mdf,
                           filename=filename)

@flask_sijax.route(app, '/itemreport/<filename>')
def item(filename):
    # Every Sijax handler function (like this one) receives at least
    # one parameter automatically, much like Python passes `self`
    # to object methods.
    # The `obj_response` parameter is the function's way of talking
    # back to the browser
    def t3(obj_response, t3):
        days = day_by_owner_only(t3, filename)
        obj_response.alert('Days are %s' % (days))
        #obj_response.html_append('#'+t3, '<li>%s</li>' % (days))

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('t3', t3)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    mdf = month_by_az(filename)
    return render_template('itembreakdown.html',
                           mdf=mdf,
                           filename=filename)