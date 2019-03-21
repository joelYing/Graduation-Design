# use lianjia;

# delete from house_deal where house_url = 'https://bj.lianjia.com/chengjiao/101103848049.html';

# mysql 查重
# select * from house_feature where house_id in (select house_id from house_feature group by house_id having count(house_id)>1);