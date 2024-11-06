from rest_framework import serializers

from vehicle.models import Car, Milage, Moto
from vehicle.validators import TitleValidator


class MilageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milage
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    last_milage = serializers.IntegerField(source='milage.all.first.milage',
                                           read_only=True)
    milage = MilageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = '__all__'


class MotoSerializer(serializers.ModelSerializer):
    last_milage = serializers.SerializerMethodField()

    class Meta:
        model = Moto
        fields = '__all__'

    def get_last_milage(self, instance):
        if instance.milage.all().first():
            return instance.milage.all().first().milage
        return 0


class MotoMilageSerializer(serializers.ModelSerializer):
    moto = MotoSerializer()

    class Meta:
        model = Milage
        fields = ('milage', 'year', 'moto',)


class MotoCreateSerializer(serializers.ModelSerializer):
    milage = MilageSerializer(many=True)  # source можно не указывать, т.к.

    # у модели Moto, есть поле  milage (related_name='milage')
    # Параметр many=True означает, что мы ожидаем список данных для каждого
    # объекта Milage, связанного с Moto.

    class Meta:
        model = Moto
        fields = '__all__'
        validators = [
            TitleValidator(field='title'),  # Валидатор на проверку названия
            serializers.UniqueTogetherValidator(
                fields=['title', 'description'],
                queryset=Moto.objects.all())  # Проверяем на уникальность
            # названия и описания
        ]

    def create(self, validated_data):
        # milage берем из validated_data и исключаем по ключевому слову milage
        # Здесь мы из validated_data вырываем этот кусок, т.е. в validated_data
        # не остается никакого объекта по ключу milage.
        milage = validated_data.pop('milage')
        # Это дает возможность создать мотоцикл из той validated_data, которая
        # нам пришла. Причем validated_data значит она уже отвалидирована,
        # значит мы можем спокойно ее записывать
        moto_item = Moto.objects.create(**validated_data)

        for m in milage:
            Milage.objects.create(**m, moto=moto_item)  # Здесь создается новый
            # пробег с указанием того, что эта ссылка на мотоцикл

        return moto_item  # Возвращаем объект
