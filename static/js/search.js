$(document).ready(
    function() {
        $('button[data-next]').click(
            function (e)
            {
                e.preventDefault();
                let n = $(this).attr('data-next');
                let classname = '.search_' + n;
                $(classname).show();
                $(this).prop("disabled", true);
                $(this).siblings('.close').hide();
            }
        );

        $('#search-btn').click
        (
            function(e) {
                e.preventDefault();
                let valid = search.validateAndSubmitForm(true);
            }
        );

        $('#search_1').blur
        (
            function() {
                if ($(this).val() !== '')
                    $(this).parent().removeClass("form-input-error");
            }
        );

        $('.close').click(function() {
            let p = $(this).parent();
            $(this).siblings('input').val('');
            let number = p.attr('class').replace("search_", "");
            $('button[data-next=' + number + ']').prop("disabled", false);
            $('.search_' + (number - 1)).find('.close').show();
            p.hide();

            search.validateAndSubmitForm(false);
        });
    }
);

var search = {

    page: 1,
    searchUrlFormatArticle: "/search/search-ajax-article?term1=R1&term2=R2&term3=R3&st=R4&exp=R5&journal=R6&page=R7",
    searchUrlFormatJournal: "/search/search-ajax-journal?term1=R1&term2=R2&term3=R3&st=R4&exp=R5&csv=R6",

    performJournalSearch: function(term1, term2, term3, st, expand, csv) {
        $('.search-results-list-journals').hide();
        $('.search-results-list-articles').hide();
        $('.search-wait').show();
        $('.search-results-container').show();

        let journal_search_url =
            this.searchUrlFormatJournal
                .replace("R1", encodeURIComponent(term1))
                .replace("R2", encodeURIComponent(term2))
                .replace("R3", encodeURIComponent(term3))
                .replace("R4", encodeURIComponent(st))
                .replace("R5", encodeURIComponent(expand))
                .replace("R6", encodeURIComponent(csv));

        $.ajax({
            cache: false,
            method: 'GET',
            url: journal_search_url,
            success: function(data) {
                $('#search-ajax-container').html(data);

                $('.search-results-item-journal a').click(
                    function(e) {
                        e.preventDefault();
                        search.performArticleSearchLink(this);
                    }
                );
            },
            complete: function() {
                $('.search-wait').hide();
                $('.search-results-list-journals').show();
            }
        });
    },

    performArticleSearchLink: function(a) {
        let link = $(a);
        let term1 = link.attr("data-term1"), term2 = link.attr("data-term2"),
            term3 = link.attr("data-term3"), st = link.attr("data-st"), journal = link.attr("data-journal");

        let page = link.attr("data-page");
        if (!page || page === "") page = "0";


        search.performArticleSearch(term1, term2, term3, st, false, journal, page);
    },

    performJournalSearchLink: function(a) {
        let link = $(a);
        let term1 = link.attr("data-term1"), term2 = link.attr("data-term2"),
            term3 = link.attr("data-term3"), st = link.attr("data-st");

        let csv = link.attr("data-csv");
        if (!csv || csv === "") csv = "";

        search.performJournalSearch(term1, term2, term3, st, false, csv);
    },

    performArticleSearch: function(term1, term2, term3, st, expand, journal, page) {
        $('.search-results-list-journals').hide();
        $('.search-results-list-articles').hide();
        $('.search-wait').show();
        $('.search-results-container').show();

        let article_search_url =
            this.searchUrlFormatArticle
                .replace("R1", encodeURIComponent(term1))
                .replace("R2", encodeURIComponent(term2))
                .replace("R3", encodeURIComponent(term3))
                .replace("R4", encodeURIComponent(st))
                .replace("R5", encodeURIComponent(expand))
                .replace("R6", encodeURIComponent(journal))
                .replace("R7", encodeURIComponent(page));

        $.ajax({
            cache: false,
            method: 'GET',
            url: article_search_url,
            success: function(data) {
                $('#search-ajax-container').html(data);
            },
            complete: function() {
                $('.search-wait').hide();
                $('.search-results-list-articles').show();

                $('.search-back a').click(
                    function(e) {
                        e.preventDefault();
                        search.performJournalSearchLink(this);
                    }
                );

                $('.article-page-link').click(
                    function(e) {
                        e.preventDefault();
                        search.performArticleSearchLink(this);
                    }
                );

                // Hack - find the link, click it.
                $('#article_page_select').change(
                    function(e) {
                        e.preventDefault();
                        let link = $('.article-page-link').first();
                        link.attr('data-page', parseInt(this.value) - 1);
                        link.click();
                    }
                );
            }
        });
    },

    validateAndSubmitForm: function(submit) {

        let t1 = $('#search_1').val(), t2 = $('#search_2').val(), t3 = $('#search_3').val(),
                    st = parseInt($('#proximity').val()) + 1, exp = false;

        let valid = (t1 !== '');

        if (valid)
        {
            if (t3 !== '')
                valid = (t2 !== '');

            if (!valid)
                $('#search_2').parent().addClass("form-input-error");
        }
        else
        {
            if (t3 !== '' && t2 === '')
                $('#search_2').parent().addClass("form-input-error");
            else
                $('#search_2').parent().removeClass("form-input-error");

            $('#search_1').parent().addClass("form-input-error");
        }

        if (valid) {
            $('#search_1').parent().removeClass("form-input-error");
            $('#search_2').parent().removeClass("form-input-error");

            if (submit)
                search.performJournalSearch(t1, t2, t3, st, exp, '');
        }
    }
}