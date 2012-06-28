
(function($) {
$.fn.adsel = function(o) {
	var me = $(this);
	if(o.cityId){
		var citySel = $('#'+o.cityId);
	}
	if(o.districtId){
		var districtSel = $('#'+o.districtId);
	}
	// ����ʡ���������option
	$.each(xzqh, function(index, province) { 
		var value = province.C
		var text = province.N;
		var newopt = '<option value="'+value+'">'+text+'</option>';
		me.append(newopt);
	})
	if(citySel){
		// ʡ��������仯ʱ�����ó����������option
		var currentProvince;
		this.each(function() {
			me.change(function(){
				citySel.find("option[value!='']").remove().end();
				districtSel.find("option[value!='']").remove().end();
				var pCode = me.val();
				if(pCode!=''){
					currentProvince = jQuery.grep(xzqh, function(province, index){
						return (province.C == pCode);
					})[0];
					$.each(currentProvince.S, function(index, city) { 
						var value = city.C
						var text = city.N;
						var newopt = '<option value="'+value+'">'+text+'</option>';
						citySel.append(newopt);
					})
				}
			});
		});
		// ����ʡ��������Ĭ��ֵ
		if(o.pValue){
			me.val(o.pValue);
			me.change();
		}
		if(districtSel){
			// ����������仯ʱ�����������������option
			var currentCity;
			citySel.change(function(){
				districtSel.find("option[value!='']").remove().end();
				var cCode = citySel.val();
				if(cCode!=''){
					currentCity = jQuery.grep(currentProvince.S, function(city, index){
						return (city.C == cCode);
					})[0];
					$.each(currentCity.S, function(index, district) { 
						var value = district.C
						var text = district.N;
						var newopt = '<option value="'+value+'">'+text+'</option>';
						districtSel.append(newopt);
					})
				}
			});
			// ���ó���������Ĭ��ֵ
			if(o.cValue){
				citySel.val(o.cValue);
				citySel.change();
			}
			// ��������������Ĭ��ֵ
			if(o.dValue){
				districtSel.val(o.dValue);
			}
		}
	}
	return false;
};
})(jQuery);