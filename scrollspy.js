$(document).ready(function() {

	$('[data-spy="scroll"]').each(function() {
		var $spy = $(this).scrollspy('refresh')
	})

	ResearchSW = true;
	TeachingSW = true;
	PublicationsSW = true;
	OthersSW = true;

	$('#ResearchBtn').click(() => {
		console.log("test1")
		$("#Research").offset({ top: $('#Research').offset().top + (ResearchSW ? 1 : 0), left: 0 });
		ResearchSW = false;
		console.log("test2")
		// $('html, body').animate({ scrollTop: $('#Research').offset().top }, timer);    
	})
	$('#TeachingBtn').click(() => {
		$("#Teaching").offset({ top: $('#Teaching').offset().top + (TeachingSW ? 1 : 0), left: 0 });
		TeachingSW = false;
		// $('html, body').animate({ scrollTop: $('#Teaching').offset().top }, timer);    
	})
	$('#PublicationsBtn').click(() => {
		$("#Publications").offset({ top: $('#Publications').offset().top + (PublicationsSW ? 1 : 0), left: 0 });
		PublicationsSW = false;
		// $('html, body').animate({ scrollTop: $('#Publications').offset().top }, timer);    
	})
	$('#OthersBtn').click(() => {
		$("#Others").offset({ top: $('#Others').offset().top + (OthersSW ? 1 : 0), left: 0 });
		OthersSW = false;
		// $('html, body').animate({ scrollTop: $('#Others').offset().top }, timer);    
	})

});


