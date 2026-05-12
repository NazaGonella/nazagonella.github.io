+++
title = "Nazareno Gonella"
author = "Nazareno Gonella"
template = "/templates/template-home.html"
+++

### Posts

---

{% for p in sections.posts | sort(attribute="date", reverse=True) %}
<p>
    {{ p.date.strftime("%d/%m/%Y") }}
    <a href="{{ p.url }}">
        {{ p.title }}
    </a>
</p>
{% endfor %}

---
