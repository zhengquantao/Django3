proverb = {
    1:["古格言", "闻过则喜，知过必改"],
    2:["古格言", "户枢不蠹，流水不腐"],
    3:["《孙子》", "知彼知己，百战不殆；不知彼而知己，一胜一负；不知彼不知己，每战必殆"],
    4:["《论语》","知之者不如好之者，好之者不如乐之者。"],
    5:["《孟子》", "不以规矩，不成方圆。"],
    6:["《庄子》", "吾生也有涯，而知也无涯"],
    7:["达尔文", "机会是每个人都有的，但许多人不知道他们已碰到它。"],
    9:["陆游", "纸上得来终觉浅，绝知此事要躬行。"],
    10:["古格言", "三军可夺帅也，匹夫不可夺志也"],
    11:["王勃", "落霞与孤鹜齐飞，秋水共长天一色"],
    12:["俗语", "鸟要紧的是翅膀，人要紧的是理想。"],
    13:["孙洙", "熟读唐诗三百首，不会作诗也会吟。"],
    14:["岳飞", "莫等闲，白了少年头，空悲切。"],
    15:["诸葛亮","非淡泊无以明志，非宁静无以致远"]

};
(function(){
    let $left_header = proverb[String(Math.floor(Math.random()*15+1))];
    let $left_body = proverb[String(Math.floor(Math.random()*15+1))];
    let $right_header = proverb[String(Math.floor(Math.random()*15+1))];
    let $right_body = proverb[String(Math.floor(Math.random()*15+1))];
    $('.left-header-1').text($left_header[0]);
    $('.left-body-1').text($left_header[1]);
    $('.left-header-2').text($left_body[0]);
    $('.left-body-2').text($left_body[1]);
    $('.right-header-1').text($right_header[0]);
    $('.right-body-1').text($right_header[1]);
    $('.right-header-2').text($right_body[0]);
    $('.right-body-2').text($right_body[1]);
})();
(setInterval(function(){
    let $left_header = proverb[String(Math.floor(Math.random()*15+1))];
    let $left_body = proverb[String(Math.floor(Math.random()*15+1))];
    let $right_header = proverb[String(Math.floor(Math.random()*15+1))];
    let $right_body = proverb[String(Math.floor(Math.random()*15+1))];
    $('.left-header-1').text($left_header[0]);
    $('.left-body-1').text($left_header[1]);
    $('.left-header-2').text($left_body[0]);
    $('.left-body-2').text($left_body[1]);
    $('.right-header-1').text($right_header[0]);
    $('.right-body-1').text($right_header[1]);
    $('.right-header-2').text($right_body[0]);
    $('.right-body-2').text($right_body[1]);
}, 3000))();