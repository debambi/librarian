% extra_scripts = '<script src="/static/js/content.js"></script>'

%# Translators, used as page title
% rebase('base.tpl', title=_('Library'))
<h1>
%# Translators, used as page heading
{{ _('Library') }}
</h1>

<div class="inner">
    <div id="tag-cloud-container" class="tag-cloud-container" data-url="{{ i18n_path(url('tags:list')) }}" data-current="{{ tag }}">
        % include('_tag_cloud')
    </div>
    <form id="pager" class="pager controls">
        <input type="hidden" name="t" value="{{ tag_id or '' }}">
        <p>
        %# Translators, used as label for search field, appears before the text box
        {{! h.vinput('q', vals, _type='text', _class='search', placeholder=_('search titles')) }}<button %# NOTE: keep together
        %# Translators, used as label for search button
            class="fake-go"><span class="icon">{{ _('go') }}</span></button>
        % if query:
        %# Translators, used as label for button that clears search results
        <a href="{{ i18n_path(request.path) }}" class="button">{{ _('clear') }}</a>
        % end
        </label>
        <span class="paging">
            % include('_simple_pager')
        </span>
        </p>
    </form>
    % if query:
    %# Translators, used as note on library page when showing search results, %(term)s represents the text typed in by user
    <p class="search-keyword">{{ _("Showing search results for '%(terms)s'") % {'terms': query} }}</p>
    % end
    <ul id="content-list" class="content-list" data-total="{{ int(pager.pages) }}">
        % include('_content_list')
    </ul>
    % if not metadata:
        <p class="empty">
        % if not query and not tag:
        %# Translators, used as note on library page when library is empty
        {{ _('Content library is currently empty') }}
        % elif query:
        %# Translators, used as note on library page when search does not return anything
        {{ _("There are no search results for '%(terms)s'") % {'terms': query} }}
        % elif tag:
        %# Translators, used as not on library page when there is no content for given tag
        {{ _("There are no results for '%(tag)s'") % {'tag': tag} }}
        % end
        </p>
    % end
</div>

<script id="loadLink" type="text/template">
    <p id="more" class="loading">
        %# Translators, link that loads more content in infinite scrolling page
        <span><button class="large special">{{ _('Load more content') }}</button></span>
    </p>
</script>

<script id="loading" type="text/template">
    <p id="loading" class="loading">
        <img src="/static/img/loading.gif">
        %# Translators, used as placeholder while infinite scrolling content is being loaded
        <span>{{ _('Loading...') }}</span>
    </p>
</script>

<script id="end" type="text/template">
    <p class="end">
    %# Translators, shown when user reaches the end of the library
    {{ _('You have reached the end of the library.') }}
    %# Translators, link that appears at the bottom of infinite-scrolling page that takes the user back to top of the page
    <a href="#content-list" class="to-top">{{ _('Go to top') }}</a>
    </p>
</script>

<script id="toTop" type="text/template">
    <div id="to-top" class="to-top">
        %# Translators, link that appears at the bottom of infinite-scrolling page that takes the user back to top of the page
        <a href="#content-list">{{ _('Go to top') }}</a>
    </div>
</script>

% include('_tag_js_templates')

