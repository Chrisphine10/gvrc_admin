--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

-- Started on 2025-09-03 11:52:19 EAT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.wards DROP CONSTRAINT wards_constituency_id_0d753ebe_fk_constitue;
ALTER TABLE ONLY public.users_user_permissions DROP CONSTRAINT users_user_permissions_user_id_92473840_fk_users_user_id;
ALTER TABLE ONLY public.users_user_permissions DROP CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm;
ALTER TABLE ONLY public.users_groups DROP CONSTRAINT users_groups_user_id_f500bee5_fk_users_user_id;
ALTER TABLE ONLY public.users_groups DROP CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id;
ALTER TABLE ONLY public.user_sessions DROP CONSTRAINT user_sessions_user_id_43ce9642_fk_users_user_id;
ALTER TABLE ONLY public.user_role_assignments DROP CONSTRAINT user_role_assignments_user_id_00c0f924_fk_users_user_id;
ALTER TABLE ONLY public.user_role_assignments DROP CONSTRAINT user_role_assignments_role_id_4e666b0f_fk_user_roles_role_id;
ALTER TABLE ONLY public.user_role_assignments DROP CONSTRAINT user_role_assignments_assigned_by_3ab02012_fk_users_user_id;
ALTER TABLE ONLY public.user_profiles DROP CONSTRAINT user_profiles_user_id_8c5ab5fe_fk_users_user_id;
ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_role_id_216516f2_fk_user_roles_role_id;
ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_permission_id_ad343843_fk_permissio;
ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_granted_by_af5d4915_fk_users_user_id;
ALTER TABLE ONLY public.music DROP CONSTRAINT music_updated_by_6e6f49a5_fk_users_user_id;
ALTER TABLE ONLY public.music_plays DROP CONSTRAINT music_plays_user_id_f5589ee3_fk_users_user_id;
ALTER TABLE ONLY public.music_plays DROP CONSTRAINT music_plays_music_id_434243a8_fk_music_music_id;
ALTER TABLE ONLY public.music DROP CONSTRAINT music_created_by_787541fa_fk_users_user_id;
ALTER TABLE ONLY public.mobile_device_usage DROP CONSTRAINT mobile_device_usage_device_id_abcd2738_fk_mobile_de;
ALTER TABLE ONLY public.facility_services DROP CONSTRAINT facility_services_service_category_id_0c249fbd_fk_service_c;
ALTER TABLE ONLY public.facility_services DROP CONSTRAINT facility_services_facility_id_9e5f55dc_fk_facilitie;
ALTER TABLE ONLY public.facility_owners DROP CONSTRAINT facility_owners_updated_by_dc292e4e_fk_users_user_id;
ALTER TABLE ONLY public.facility_owners DROP CONSTRAINT facility_owners_owner_type_id_7dea0d2c_fk_owner_typ;
ALTER TABLE ONLY public.facility_owners DROP CONSTRAINT facility_owners_facility_id_36e99bf4_fk_facilities_facility_id;
ALTER TABLE ONLY public.facility_owners DROP CONSTRAINT facility_owners_created_by_6c9f6f73_fk_users_user_id;
ALTER TABLE ONLY public.facility_infrastructure DROP CONSTRAINT facility_infrastructure_updated_by_91040b96_fk_users_user_id;
ALTER TABLE ONLY public.facility_infrastructure DROP CONSTRAINT facility_infrastructure_created_by_003846c8_fk_users_user_id;
ALTER TABLE ONLY public.facility_infrastructure DROP CONSTRAINT facility_infrastruct_infrastructure_type__c1c3a8d3_fk_infrastru;
ALTER TABLE ONLY public.facility_infrastructure DROP CONSTRAINT facility_infrastruct_facility_id_42b8797f_fk_facilitie;
ALTER TABLE ONLY public.facility_infrastructure DROP CONSTRAINT facility_infrastruct_condition_status_id_382dd3f9_fk_condition;
ALTER TABLE ONLY public.facility_gbv_categories DROP CONSTRAINT facility_gbv_categories_created_by_b61c6e4f_fk_users_user_id;
ALTER TABLE ONLY public.facility_gbv_categories DROP CONSTRAINT facility_gbv_categor_gbv_category_id_3b6325a7_fk_gbv_categ;
ALTER TABLE ONLY public.facility_gbv_categories DROP CONSTRAINT facility_gbv_categor_facility_id_0cf99a99_fk_facilitie;
ALTER TABLE ONLY public.facility_coordinates DROP CONSTRAINT facility_coordinates_facility_id_d2e67c35_fk_facilitie;
ALTER TABLE ONLY public.facility_contacts DROP CONSTRAINT facility_contacts_updated_by_f3e4a7e0_fk_users_user_id;
ALTER TABLE ONLY public.facility_contacts DROP CONSTRAINT facility_contacts_facility_id_c91b40ee_fk_facilitie;
ALTER TABLE ONLY public.facility_contacts DROP CONSTRAINT facility_contacts_created_by_a5f8561c_fk_users_user_id;
ALTER TABLE ONLY public.facility_contacts DROP CONSTRAINT facility_contacts_contact_type_id_5380d0c8_fk_contact_t;
ALTER TABLE ONLY public.facilities DROP CONSTRAINT facilities_ward_id_b19cbd31_fk_wards_ward_id;
ALTER TABLE ONLY public.facilities DROP CONSTRAINT facilities_updated_by_c7d06497_fk_users_user_id;
ALTER TABLE ONLY public.facilities DROP CONSTRAINT facilities_operational_status_i_946bd007_fk_operation;
ALTER TABLE ONLY public.facilities DROP CONSTRAINT facilities_created_by_522b765d_fk_users_user_id;
ALTER TABLE ONLY public.emergency_chat_notifications DROP CONSTRAINT emergency_chat_notifications_user_id_c5187218_fk_users_user_id;
ALTER TABLE ONLY public.emergency_chat_notifications DROP CONSTRAINT emergency_chat_notif_message_id_d4d8bfe6_fk_emergency;
ALTER TABLE ONLY public.emergency_chat_notifications DROP CONSTRAINT emergency_chat_notif_conversation_id_ddf27239_fk_emergency;
ALTER TABLE ONLY public.emergency_chat_messages DROP CONSTRAINT emergency_chat_messages_sender_id_3f59dcfd_fk_users_user_id;
ALTER TABLE ONLY public.emergency_chat_messages DROP CONSTRAINT emergency_chat_messa_conversation_id_4702a48a_fk_emergency;
ALTER TABLE ONLY public.emergency_chat_conversations DROP CONSTRAINT emergency_chat_conve_mobile_session_id_58959a4d_fk_mobile_de;
ALTER TABLE ONLY public.emergency_chat_conversations DROP CONSTRAINT emergency_chat_conve_last_message_by_id_72260c9b_fk_users_use;
ALTER TABLE ONLY public.emergency_chat_conversations DROP CONSTRAINT emergency_chat_conve_assigned_admin_id_c2c47763_fk_users_use;
ALTER TABLE ONLY public.documents DROP CONSTRAINT documents_uploaded_by_fa4ffa51_fk_users_user_id;
ALTER TABLE ONLY public.documents DROP CONSTRAINT documents_gbv_category_c51e0c9d_fk_gbv_categ;
ALTER TABLE ONLY public.documents DROP CONSTRAINT documents_document_type_id_44d85642_fk_document_;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_user_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.custom_tokens DROP CONSTRAINT custom_tokens_user_id_57e20417_fk_users_user_id;
ALTER TABLE ONLY public.contact_interactions DROP CONSTRAINT contact_interactions_device_id_aedd942e_fk_mobile_de;
ALTER TABLE ONLY public.contact_interactions DROP CONSTRAINT contact_interactions_contact_id_f5f4544a_fk_facility_;
ALTER TABLE ONLY public.constituencies DROP CONSTRAINT constituencies_county_id_308f52ae_fk_counties_county_id;
ALTER TABLE ONLY public.authtoken_token DROP CONSTRAINT authtoken_token_user_id_35299eff_fk_users_user_id;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE ONLY public.audit_trail DROP CONSTRAINT audit_trail_session_id_43235492_fk_user_sessions_session_id;
ALTER TABLE ONLY public.api_tokens DROP CONSTRAINT api_tokens_user_id_2db24e1c_fk_users_user_id;
DROP INDEX public.wards_ward_na_8e1694_idx;
DROP INDEX public.wards_ward_code_164705e5_like;
DROP INDEX public.wards_ward_co_61edb7_idx;
DROP INDEX public.wards_constituency_id_0d753ebe;
DROP INDEX public.wards_constit_b3144c_idx;
DROP INDEX public.users_username_e8658fc8_like;
DROP INDEX public.users_user_permissions_user_id_92473840;
DROP INDEX public.users_user_permissions_permission_id_6d08dcd2;
DROP INDEX public.users_phone_number_b4cde146_like;
DROP INDEX public.users_groups_user_id_f500bee5;
DROP INDEX public.users_groups_group_id_2f3517aa;
DROP INDEX public.users_email_0ea73cca_like;
DROP INDEX public.user_sessions_user_id_43ce9642;
DROP INDEX public.user_sessions_session_id_b4ebe5e4_like;
DROP INDEX public.user_sessio_user_id_eb20aa_idx;
DROP INDEX public.user_sessio_is_acti_1b3cb1_idx;
DROP INDEX public.user_sessio_expires_66ae96_idx;
DROP INDEX public.user_roles_role_name_1bf67ad3_like;
DROP INDEX public.user_role_assignments_user_id_00c0f924;
DROP INDEX public.user_role_assignments_role_id_4e666b0f;
DROP INDEX public.user_role_assignments_assigned_by_3ab02012;
DROP INDEX public.service_categories_category_name_e069a484_like;
DROP INDEX public.service_cat_categor_322cb1_idx;
DROP INDEX public.role_permissions_role_id_216516f2;
DROP INDEX public.role_permissions_permission_id_ad343843;
DROP INDEX public.role_permissions_granted_by_af5d4915;
DROP INDEX public.permissions_permission_name_6ba3c52f_like;
DROP INDEX public.owner_types_type_name_d3393f45_like;
DROP INDEX public.owner_types_type_na_c589c3_idx;
DROP INDEX public.operational_statuses_status_name_acac0c8e_like;
DROP INDEX public.operational_status__0bbf1d_idx;
DROP INDEX public.operational_sort_or_617ed2_idx;
DROP INDEX public.music_updated_by_6e6f49a5;
DROP INDEX public.music_plays_user_id_f5589ee3;
DROP INDEX public.music_plays_user_id_4711ae_idx;
DROP INDEX public.music_plays_played__8346ff_idx;
DROP INDEX public.music_plays_music_id_434243a8;
DROP INDEX public.music_plays_music_i_a83db1_idx;
DROP INDEX public.music_is_acti_040a4a_idx;
DROP INDEX public.music_genre_148897_idx;
DROP INDEX public.music_created_by_787541fa;
DROP INDEX public.music_created_88f77f_idx;
DROP INDEX public.mobile_device_usage_device_id_abcd2738_like;
DROP INDEX public.mobile_device_usage_device_id_abcd2738;
DROP INDEX public.mobile_device_sessions_device_id_706334c7_like;
DROP INDEX public.mobile_devi_preferr_c75d7d_idx;
DROP INDEX public.mobile_devi_locatio_228e3a_idx;
DROP INDEX public.mobile_devi_last_ac_6b5072_idx;
DROP INDEX public.mobile_devi_is_acti_20527c_idx;
DROP INDEX public.mobile_devi_first_u_3c06ea_idx;
DROP INDEX public.mobile_devi_feature_d5c975_idx;
DROP INDEX public.mobile_devi_feature_78b551_idx;
DROP INDEX public.mobile_devi_device__b7f94d_idx;
DROP INDEX public.infrastructure_types_type_name_46d1539d_like;
DROP INDEX public.infrastruct_type_na_52876f_idx;
DROP INDEX public.gbv_categories_category_name_9002d128_like;
DROP INDEX public.gbv_categor_categor_3ededf_idx;
DROP INDEX public.facility_services_service_category_id_0c249fbd;
DROP INDEX public.facility_services_facility_id_9e5f55dc;
DROP INDEX public.facility_se_service_a2b980_idx;
DROP INDEX public.facility_se_is_acti_a1e033_idx;
DROP INDEX public.facility_se_facilit_c92597_idx;
DROP INDEX public.facility_owners_updated_by_dc292e4e;
DROP INDEX public.facility_owners_owner_type_id_7dea0d2c;
DROP INDEX public.facility_owners_facility_id_36e99bf4;
DROP INDEX public.facility_owners_created_by_6c9f6f73;
DROP INDEX public.facility_ow_owner_t_a26f8d_idx;
DROP INDEX public.facility_ow_facilit_21de47_idx;
DROP INDEX public.facility_infrastructure_updated_by_91040b96;
DROP INDEX public.facility_infrastructure_infrastructure_type_id_c1c3a8d3;
DROP INDEX public.facility_infrastructure_facility_id_42b8797f;
DROP INDEX public.facility_infrastructure_created_by_003846c8;
DROP INDEX public.facility_infrastructure_condition_status_id_382dd3f9;
DROP INDEX public.facility_in_is_acti_354d9a_idx;
DROP INDEX public.facility_in_infrast_970d40_idx;
DROP INDEX public.facility_in_facilit_3980d5_idx;
DROP INDEX public.facility_in_conditi_1ec089_idx;
DROP INDEX public.facility_gbv_categories_gbv_category_id_3b6325a7;
DROP INDEX public.facility_gbv_categories_facility_id_0cf99a99;
DROP INDEX public.facility_gbv_categories_created_by_b61c6e4f;
DROP INDEX public.facility_gb_gbv_cat_c7e042_idx;
DROP INDEX public.facility_gb_facilit_2a099c_idx;
DROP INDEX public.facility_coordinates_facility_id_d2e67c35;
DROP INDEX public.facility_contacts_updated_by_f3e4a7e0;
DROP INDEX public.facility_contacts_facility_id_c91b40ee;
DROP INDEX public.facility_contacts_created_by_a5f8561c;
DROP INDEX public.facility_contacts_contact_type_id_5380d0c8;
DROP INDEX public.facility_co_is_prim_a3bcec_idx;
DROP INDEX public.facility_co_facilit_72d18d_idx;
DROP INDEX public.facility_co_facilit_12040b_idx;
DROP INDEX public.facility_co_contact_805b0e_idx;
DROP INDEX public.facility_co_collect_67ee0c_idx;
DROP INDEX public.facilities_ward_id_b19cbd31;
DROP INDEX public.facilities_ward_id_93b6d2_idx;
DROP INDEX public.facilities_updated_by_c7d06497;
DROP INDEX public.facilities_registration_number_22655837_like;
DROP INDEX public.facilities_operational_status_id_946bd007;
DROP INDEX public.facilities_operati_28f767_idx;
DROP INDEX public.facilities_is_acti_76f1be_idx;
DROP INDEX public.facilities_facility_code_a17644aa_like;
DROP INDEX public.facilities_created_by_522b765d;
DROP INDEX public.emergency_chat_notifications_user_id_c5187218;
DROP INDEX public.emergency_chat_notifications_message_id_d4d8bfe6;
DROP INDEX public.emergency_chat_notifications_conversation_id_ddf27239;
DROP INDEX public.emergency_chat_messages_sender_id_3f59dcfd;
DROP INDEX public.emergency_chat_messages_conversation_id_4702a48a;
DROP INDEX public.emergency_chat_conversations_mobile_session_id_58959a4d_like;
DROP INDEX public.emergency_chat_conversations_mobile_session_id_58959a4d;
DROP INDEX public.emergency_chat_conversations_last_message_by_id_72260c9b;
DROP INDEX public.emergency_chat_conversations_assigned_admin_id_c2c47763;
DROP INDEX public.emergency_c_user_id_611b40_idx;
DROP INDEX public.emergency_c_status_dc2d02_idx;
DROP INDEX public.emergency_c_status_51cf71_idx;
DROP INDEX public.emergency_c_sent_at_3a3fbe_idx;
DROP INDEX public.emergency_c_sender__568497_idx;
DROP INDEX public.emergency_c_sender__3b2a87_idx;
DROP INDEX public.emergency_c_priorit_4bd477_idx;
DROP INDEX public.emergency_c_notific_98f949_idx;
DROP INDEX public.emergency_c_last_me_8a2ac0_idx;
DROP INDEX public.emergency_c_is_urge_d9f777_idx;
DROP INDEX public.emergency_c_is_read_7681b4_idx;
DROP INDEX public.emergency_c_created_cfae1d_idx;
DROP INDEX public.emergency_c_created_6bac2d_idx;
DROP INDEX public.emergency_c_convers_facbbe_idx;
DROP INDEX public.emergency_c_assigne_def626_idx;
DROP INDEX public.documents_uploaded_by_fa4ffa51;
DROP INDEX public.documents_uploade_f550b6_idx;
DROP INDEX public.documents_is_publ_af3237_idx;
DROP INDEX public.documents_is_acti_a803bb_idx;
DROP INDEX public.documents_gbv_category_c51e0c9d;
DROP INDEX public.documents_document_type_id_44d85642;
DROP INDEX public.documents_documen_0426e4_idx;
DROP INDEX public.document_types_type_name_09b23418_like;
DROP INDEX public.document_ty_type_na_0d5fea_idx;
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.custom_tokens_key_e2c9d401_like;
DROP INDEX public.counties_county_code_fde4d419_like;
DROP INDEX public.counties_county__a59c4f_idx;
DROP INDEX public.counties_county__94451a_idx;
DROP INDEX public.contact_types_type_name_d45844b9_like;
DROP INDEX public.contact_typ_type_na_65c398_idx;
DROP INDEX public.contact_interactions_device_id_aedd942e_like;
DROP INDEX public.contact_interactions_device_id_aedd942e;
DROP INDEX public.contact_interactions_contact_id_f5f4544a;
DROP INDEX public.constituencies_county_id_308f52ae;
DROP INDEX public.constituencies_constituency_code_9423bb36_like;
DROP INDEX public.constituenc_county__9dc793_idx;
DROP INDEX public.constituenc_constit_e8225b_idx;
DROP INDEX public.constituenc_constit_b8037d_idx;
DROP INDEX public.condition_statuses_status_name_1f4362dd_like;
DROP INDEX public.condition_s_status__6509be_idx;
DROP INDEX public.authtoken_token_key_10f0b77e_like;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
DROP INDEX public.audit_trail_session_id_43235492_like;
DROP INDEX public.audit_trail_session_id_43235492;
DROP INDEX public.api_tokens_user_id_caf836_idx;
DROP INDEX public.api_tokens_user_id_2db24e1c;
DROP INDEX public.api_tokens_token_hash_70d52dcc_like;
DROP INDEX public.api_tokens_is_acti_949075_idx;
DROP INDEX public.api_tokens_expires_a047d2_idx;
ALTER TABLE ONLY public.wards DROP CONSTRAINT wards_ward_code_key;
ALTER TABLE ONLY public.wards DROP CONSTRAINT wards_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
ALTER TABLE ONLY public.users_user_permissions DROP CONSTRAINT users_user_permissions_user_id_permission_id_3b86cbdf_uniq;
ALTER TABLE ONLY public.users_user_permissions DROP CONSTRAINT users_user_permissions_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_phone_number_key;
ALTER TABLE ONLY public.users_groups DROP CONSTRAINT users_groups_user_id_group_id_fc7788e8_uniq;
ALTER TABLE ONLY public.users_groups DROP CONSTRAINT users_groups_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
ALTER TABLE ONLY public.user_sessions DROP CONSTRAINT user_sessions_pkey;
ALTER TABLE ONLY public.user_roles DROP CONSTRAINT user_roles_role_name_key;
ALTER TABLE ONLY public.user_roles DROP CONSTRAINT user_roles_pkey;
ALTER TABLE ONLY public.user_role_assignments DROP CONSTRAINT user_role_assignments_user_id_role_id_db8b4891_uniq;
ALTER TABLE ONLY public.user_role_assignments DROP CONSTRAINT user_role_assignments_pkey;
ALTER TABLE ONLY public.user_profiles DROP CONSTRAINT user_profiles_user_id_key;
ALTER TABLE ONLY public.user_profiles DROP CONSTRAINT user_profiles_pkey;
ALTER TABLE ONLY public.service_categories DROP CONSTRAINT service_categories_pkey;
ALTER TABLE ONLY public.service_categories DROP CONSTRAINT service_categories_category_name_key;
ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_role_id_permission_id_04f77df0_uniq;
ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_pkey;
ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_pkey;
ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_permission_name_key;
ALTER TABLE ONLY public.owner_types DROP CONSTRAINT owner_types_type_name_key;
ALTER TABLE ONLY public.owner_types DROP CONSTRAINT owner_types_pkey;
ALTER TABLE ONLY public.operational_statuses DROP CONSTRAINT operational_statuses_status_name_key;
ALTER TABLE ONLY public.operational_statuses DROP CONSTRAINT operational_statuses_pkey;
ALTER TABLE ONLY public.music_plays DROP CONSTRAINT music_plays_pkey;
ALTER TABLE ONLY public.music DROP CONSTRAINT music_pkey;
ALTER TABLE ONLY public.mobile_device_usage DROP CONSTRAINT mobile_device_usage_pkey;
ALTER TABLE ONLY public.mobile_device_usage DROP CONSTRAINT mobile_device_usage_device_id_feature_name_2689baf9_uniq;
ALTER TABLE ONLY public.mobile_device_sessions DROP CONSTRAINT mobile_device_sessions_pkey;
ALTER TABLE ONLY public.infrastructure_types DROP CONSTRAINT infrastructure_types_type_name_key;
ALTER TABLE ONLY public.infrastructure_types DROP CONSTRAINT infrastructure_types_pkey;
ALTER TABLE ONLY public.gbv_categories DROP CONSTRAINT gbv_categories_pkey;
ALTER TABLE ONLY public.gbv_categories DROP CONSTRAINT gbv_categories_category_name_key;
ALTER TABLE ONLY public.facility_services DROP CONSTRAINT facility_services_pkey;
ALTER TABLE ONLY public.facility_owners DROP CONSTRAINT facility_owners_pkey;
ALTER TABLE ONLY public.facility_infrastructure DROP CONSTRAINT facility_infrastructure_pkey;
ALTER TABLE ONLY public.facility_gbv_categories DROP CONSTRAINT facility_gbv_categories_pkey;
ALTER TABLE ONLY public.facility_gbv_categories DROP CONSTRAINT facility_gbv_categories_facility_id_gbv_category_568d54e0_uniq;
ALTER TABLE ONLY public.facility_coordinates DROP CONSTRAINT facility_coordinates_pkey;
ALTER TABLE ONLY public.facility_contacts DROP CONSTRAINT facility_contacts_pkey;
ALTER TABLE ONLY public.facilities DROP CONSTRAINT facilities_registration_number_key;
ALTER TABLE ONLY public.facilities DROP CONSTRAINT facilities_pkey;
ALTER TABLE ONLY public.facilities DROP CONSTRAINT facilities_facility_code_key;
ALTER TABLE ONLY public.emergency_chat_notifications DROP CONSTRAINT emergency_chat_notifications_pkey;
ALTER TABLE ONLY public.emergency_chat_messages DROP CONSTRAINT emergency_chat_messages_pkey;
ALTER TABLE ONLY public.emergency_chat_conversations DROP CONSTRAINT emergency_chat_conversations_pkey;
ALTER TABLE ONLY public.documents DROP CONSTRAINT documents_pkey;
ALTER TABLE ONLY public.document_types DROP CONSTRAINT document_types_type_name_key;
ALTER TABLE ONLY public.document_types DROP CONSTRAINT document_types_pkey;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.custom_tokens DROP CONSTRAINT custom_tokens_user_id_key;
ALTER TABLE ONLY public.custom_tokens DROP CONSTRAINT custom_tokens_pkey;
ALTER TABLE ONLY public.counties DROP CONSTRAINT counties_pkey;
ALTER TABLE ONLY public.counties DROP CONSTRAINT counties_county_code_key;
ALTER TABLE ONLY public.contact_types DROP CONSTRAINT contact_types_type_name_key;
ALTER TABLE ONLY public.contact_types DROP CONSTRAINT contact_types_pkey;
ALTER TABLE ONLY public.contact_interactions DROP CONSTRAINT contact_interactions_pkey;
ALTER TABLE ONLY public.constituencies DROP CONSTRAINT constituencies_pkey;
ALTER TABLE ONLY public.constituencies DROP CONSTRAINT constituencies_constituency_code_key;
ALTER TABLE ONLY public.condition_statuses DROP CONSTRAINT condition_statuses_status_name_key;
ALTER TABLE ONLY public.condition_statuses DROP CONSTRAINT condition_statuses_pkey;
ALTER TABLE ONLY public.authtoken_token DROP CONSTRAINT authtoken_token_user_id_key;
ALTER TABLE ONLY public.authtoken_token DROP CONSTRAINT authtoken_token_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
ALTER TABLE ONLY public.audit_trail DROP CONSTRAINT audit_trail_pkey;
ALTER TABLE ONLY public.api_tokens DROP CONSTRAINT api_tokens_token_hash_key;
ALTER TABLE ONLY public.api_tokens DROP CONSTRAINT api_tokens_pkey;
DROP TABLE public.wards;
DROP TABLE public.users_user_permissions;
DROP TABLE public.users_groups;
DROP TABLE public.users;
DROP TABLE public.user_sessions;
DROP TABLE public.user_roles;
DROP TABLE public.user_role_assignments;
DROP TABLE public.user_profiles;
DROP TABLE public.service_categories;
DROP TABLE public.role_permissions;
DROP TABLE public.permissions;
DROP TABLE public.owner_types;
DROP TABLE public.operational_statuses;
DROP TABLE public.music_plays;
DROP TABLE public.music;
DROP TABLE public.mobile_device_usage;
DROP TABLE public.mobile_device_sessions;
DROP TABLE public.infrastructure_types;
DROP TABLE public.gbv_categories;
DROP TABLE public.facility_services;
DROP TABLE public.facility_owners;
DROP TABLE public.facility_infrastructure;
DROP TABLE public.facility_gbv_categories;
DROP TABLE public.facility_coordinates;
DROP TABLE public.facility_contacts;
DROP TABLE public.facilities;
DROP TABLE public.emergency_chat_notifications;
DROP TABLE public.emergency_chat_messages;
DROP TABLE public.emergency_chat_conversations;
DROP TABLE public.documents;
DROP TABLE public.document_types;
DROP TABLE public.django_session;
DROP TABLE public.django_migrations;
DROP TABLE public.django_content_type;
DROP TABLE public.django_admin_log;
DROP TABLE public.custom_tokens;
DROP TABLE public.counties;
DROP TABLE public.contact_types;
DROP TABLE public.contact_interactions;
DROP TABLE public.constituencies;
DROP TABLE public.condition_statuses;
DROP TABLE public.authtoken_token;
DROP TABLE public.auth_permission;
DROP TABLE public.auth_group_permissions;
DROP TABLE public.auth_group;
DROP TABLE public.audit_trail;
DROP TABLE public.api_tokens;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 239 (class 1259 OID 67079)
-- Name: api_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.api_tokens (
    token_id integer NOT NULL,
    token_name character varying(100) NOT NULL,
    token_hash character varying(255) NOT NULL,
    last_used_at timestamp with time zone,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- TOC entry 238 (class 1259 OID 67078)
-- Name: api_tokens_token_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.api_tokens ALTER COLUMN token_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.api_tokens_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 287 (class 1259 OID 67598)
-- Name: audit_trail; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_trail (
    audit_id bigint NOT NULL,
    table_name character varying(50) NOT NULL,
    record_id bigint NOT NULL,
    action_type character varying(20) NOT NULL,
    event_category character varying(20) NOT NULL,
    ip_address inet,
    old_values jsonb NOT NULL,
    new_values jsonb NOT NULL,
    changed_fields jsonb NOT NULL,
    severity_level character varying(10) NOT NULL,
    description text NOT NULL,
    justification text NOT NULL,
    failure_reason text NOT NULL,
    metadata jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    session_id character varying(128)
);


--
-- TOC entry 286 (class 1259 OID 67597)
-- Name: audit_trail_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.audit_trail ALTER COLUMN audit_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.audit_trail_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 222 (class 1259 OID 66980)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- TOC entry 221 (class 1259 OID 66979)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 224 (class 1259 OID 66988)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- TOC entry 223 (class 1259 OID 66987)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 220 (class 1259 OID 66974)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- TOC entry 219 (class 1259 OID 66973)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 290 (class 1259 OID 67641)
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- TOC entry 251 (class 1259 OID 67262)
-- Name: condition_statuses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.condition_statuses (
    condition_status_id integer NOT NULL,
    status_name character varying(50) NOT NULL,
    description character varying(255) NOT NULL
);


--
-- TOC entry 250 (class 1259 OID 67261)
-- Name: condition_statuses_condition_status_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.condition_statuses ALTER COLUMN condition_status_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.condition_statuses_condition_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 269 (class 1259 OID 67359)
-- Name: constituencies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.constituencies (
    constituency_id integer NOT NULL,
    constituency_name character varying(100) NOT NULL,
    constituency_code character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    county_id integer NOT NULL
);


--
-- TOC entry 268 (class 1259 OID 67358)
-- Name: constituencies_constituency_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.constituencies ALTER COLUMN constituency_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.constituencies_constituency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 289 (class 1259 OID 67606)
-- Name: contact_interactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contact_interactions (
    interaction_id integer NOT NULL,
    user_latitude numeric(10,8),
    user_longitude numeric(11,8),
    is_helpful boolean,
    created_at timestamp with time zone NOT NULL,
    contact_id integer NOT NULL,
    device_id character varying(128),
    click_data jsonb NOT NULL,
    interaction_type character varying(50) NOT NULL
);


--
-- TOC entry 288 (class 1259 OID 67605)
-- Name: contact_interactions_interaction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.contact_interactions ALTER COLUMN interaction_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.contact_interactions_interaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 253 (class 1259 OID 67270)
-- Name: contact_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contact_types (
    contact_type_id integer NOT NULL,
    type_name character varying(50) NOT NULL,
    validation_regex character varying(255) NOT NULL
);


--
-- TOC entry 252 (class 1259 OID 67269)
-- Name: contact_types_contact_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.contact_types ALTER COLUMN contact_type_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.contact_types_contact_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 267 (class 1259 OID 67351)
-- Name: counties; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.counties (
    county_id integer NOT NULL,
    county_name character varying(100) NOT NULL,
    county_code character varying(10) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


--
-- TOC entry 266 (class 1259 OID 67350)
-- Name: counties_county_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.counties ALTER COLUMN county_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.counties_county_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 235 (class 1259 OID 67061)
-- Name: custom_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.custom_tokens (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- TOC entry 246 (class 1259 OID 67210)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- TOC entry 245 (class 1259 OID 67209)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 218 (class 1259 OID 66966)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- TOC entry 217 (class 1259 OID 66965)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 216 (class 1259 OID 66958)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- TOC entry 215 (class 1259 OID 66957)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 303 (class 1259 OID 67840)
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- TOC entry 255 (class 1259 OID 67278)
-- Name: document_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_types (
    document_type_id integer NOT NULL,
    type_name character varying(50) NOT NULL,
    allowed_extensions character varying(255) NOT NULL,
    max_file_size_mb integer NOT NULL,
    description character varying(255) NOT NULL
);


--
-- TOC entry 254 (class 1259 OID 67277)
-- Name: document_types_document_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.document_types ALTER COLUMN document_type_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.document_types_document_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 298 (class 1259 OID 67744)
-- Name: documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.documents (
    document_id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    file_url character varying(500) NOT NULL,
    file_name character varying(255) NOT NULL,
    file_size_bytes bigint,
    content text NOT NULL,
    image_url character varying(500) NOT NULL,
    external_url character varying(500) NOT NULL,
    is_public boolean NOT NULL,
    is_active boolean NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    document_type_id integer NOT NULL,
    gbv_category integer,
    uploaded_by integer NOT NULL,
    file character varying(100)
);


--
-- TOC entry 297 (class 1259 OID 67743)
-- Name: documents_document_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.documents ALTER COLUMN document_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.documents_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 292 (class 1259 OID 67656)
-- Name: emergency_chat_conversations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.emergency_chat_conversations (
    conversation_id integer NOT NULL,
    status character varying(20) NOT NULL,
    priority character varying(20) NOT NULL,
    subject character varying(200) NOT NULL,
    last_message text NOT NULL,
    last_message_at timestamp with time zone,
    unread_count_mobile integer NOT NULL,
    unread_count_admin integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    assigned_admin_id integer,
    last_message_by_id integer,
    mobile_session_id character varying(128) NOT NULL
);


--
-- TOC entry 291 (class 1259 OID 67655)
-- Name: emergency_chat_conversations_conversation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.emergency_chat_conversations ALTER COLUMN conversation_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.emergency_chat_conversations_conversation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 294 (class 1259 OID 67664)
-- Name: emergency_chat_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.emergency_chat_messages (
    message_id integer NOT NULL,
    sender_type character varying(20) NOT NULL,
    content text NOT NULL,
    message_type character varying(20) NOT NULL,
    media_file character varying(100),
    media_url character varying(200) NOT NULL,
    status character varying(20) NOT NULL,
    sent_at timestamp with time zone NOT NULL,
    delivered_at timestamp with time zone,
    read_at timestamp with time zone,
    is_urgent boolean NOT NULL,
    metadata jsonb NOT NULL,
    conversation_id integer NOT NULL,
    sender_id integer
);


--
-- TOC entry 293 (class 1259 OID 67663)
-- Name: emergency_chat_messages_message_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.emergency_chat_messages ALTER COLUMN message_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.emergency_chat_messages_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 296 (class 1259 OID 67672)
-- Name: emergency_chat_notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.emergency_chat_notifications (
    notification_id integer NOT NULL,
    notification_type character varying(30) NOT NULL,
    title character varying(200) NOT NULL,
    body text NOT NULL,
    is_read boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    conversation_id integer NOT NULL,
    message_id integer
);


--
-- TOC entry 295 (class 1259 OID 67671)
-- Name: emergency_chat_notifications_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.emergency_chat_notifications ALTER COLUMN notification_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.emergency_chat_notifications_notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 273 (class 1259 OID 67398)
-- Name: facilities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facilities (
    facility_id integer NOT NULL,
    facility_name character varying(200) NOT NULL,
    facility_code character varying(50) NOT NULL,
    registration_number character varying(100) NOT NULL,
    address_line_1 character varying(255) NOT NULL,
    address_line_2 character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    description text NOT NULL,
    website_url character varying(500) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    created_by integer NOT NULL,
    operational_status_id integer NOT NULL,
    updated_by integer,
    ward_id integer NOT NULL
);


--
-- TOC entry 272 (class 1259 OID 67397)
-- Name: facilities_facility_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.facilities ALTER COLUMN facility_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.facilities_facility_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 275 (class 1259 OID 67410)
-- Name: facility_contacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facility_contacts (
    contact_id integer NOT NULL,
    contact_value character varying(255) NOT NULL,
    contact_person_name character varying(100) NOT NULL,
    is_primary boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    contact_type_id integer NOT NULL,
    created_by integer NOT NULL,
    facility_id integer NOT NULL,
    updated_by integer
);


--
-- TOC entry 274 (class 1259 OID 67409)
-- Name: facility_contacts_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.facility_contacts ALTER COLUMN contact_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.facility_contacts_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 277 (class 1259 OID 67416)
-- Name: facility_coordinates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facility_coordinates (
    coordinate_id integer NOT NULL,
    latitude numeric(10,8) NOT NULL,
    longitude numeric(11,8) NOT NULL,
    collection_date date NOT NULL,
    data_source character varying(100) NOT NULL,
    collection_method character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    facility_id integer NOT NULL
);


--
-- TOC entry 276 (class 1259 OID 67415)
-- Name: facility_coordinates_coordinate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.facility_coordinates ALTER COLUMN coordinate_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.facility_coordinates_coordinate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 279 (class 1259 OID 67422)
-- Name: facility_gbv_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facility_gbv_categories (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by integer NOT NULL,
    facility_id integer NOT NULL,
    gbv_category_id integer NOT NULL
);


--
-- TOC entry 278 (class 1259 OID 67421)
-- Name: facility_gbv_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.facility_gbv_categories ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.facility_gbv_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 281 (class 1259 OID 67428)
-- Name: facility_infrastructure; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facility_infrastructure (
    infrastructure_id integer NOT NULL,
    description text NOT NULL,
    capacity integer,
    current_utilization integer,
    is_available boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    condition_status_id integer NOT NULL,
    facility_id integer NOT NULL,
    infrastructure_type_id integer NOT NULL,
    created_by integer,
    is_active boolean NOT NULL,
    updated_by integer
);


--
-- TOC entry 280 (class 1259 OID 67427)
-- Name: facility_infrastructure_infrastructure_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.facility_infrastructure ALTER COLUMN infrastructure_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.facility_infrastructure_infrastructure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 283 (class 1259 OID 67436)
-- Name: facility_owners; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facility_owners (
    owner_id integer NOT NULL,
    owner_name character varying(200) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    created_by integer NOT NULL,
    facility_id integer NOT NULL,
    owner_type_id integer NOT NULL,
    updated_by integer
);


--
-- TOC entry 282 (class 1259 OID 67435)
-- Name: facility_owners_owner_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.facility_owners ALTER COLUMN owner_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.facility_owners_owner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 285 (class 1259 OID 67442)
-- Name: facility_services; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facility_services (
    service_id integer NOT NULL,
    service_name character varying(200) NOT NULL,
    service_description text NOT NULL,
    is_free boolean NOT NULL,
    cost_range character varying(100) NOT NULL,
    currency character varying(3) NOT NULL,
    availability_hours character varying(200) NOT NULL,
    availability_days character varying(100) NOT NULL,
    appointment_required boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    facility_id integer NOT NULL,
    service_category_id integer NOT NULL
);


--
-- TOC entry 284 (class 1259 OID 67441)
-- Name: facility_services_service_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.facility_services ALTER COLUMN service_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.facility_services_service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 257 (class 1259 OID 67288)
-- Name: gbv_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gbv_categories (
    gbv_category_id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    description character varying(500) NOT NULL,
    icon_url character varying(500) NOT NULL
);


--
-- TOC entry 256 (class 1259 OID 67287)
-- Name: gbv_categories_gbv_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.gbv_categories ALTER COLUMN gbv_category_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.gbv_categories_gbv_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 259 (class 1259 OID 67298)
-- Name: infrastructure_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.infrastructure_types (
    infrastructure_type_id integer NOT NULL,
    type_name character varying(100) NOT NULL,
    description character varying(500) NOT NULL
);


--
-- TOC entry 258 (class 1259 OID 67297)
-- Name: infrastructure_types_infrastructure_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.infrastructure_types ALTER COLUMN infrastructure_type_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.infrastructure_types_infrastructure_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 247 (class 1259 OID 67230)
-- Name: mobile_device_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mobile_device_sessions (
    device_id character varying(128) NOT NULL,
    notification_enabled boolean NOT NULL,
    dark_mode_enabled boolean NOT NULL,
    preferred_language character varying(5) NOT NULL,
    latitude numeric(10,8),
    longitude numeric(11,8),
    location_updated_at timestamp with time zone,
    location_permission_granted boolean NOT NULL,
    is_active boolean NOT NULL,
    last_active_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    game_high_score integer NOT NULL
);


--
-- TOC entry 249 (class 1259 OID 67236)
-- Name: mobile_device_usage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mobile_device_usage (
    usage_id integer NOT NULL,
    feature_name character varying(100) NOT NULL,
    feature_category character varying(50) NOT NULL,
    usage_count integer NOT NULL,
    first_used timestamp with time zone NOT NULL,
    last_used timestamp with time zone NOT NULL,
    additional_data jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    device_id character varying(128) NOT NULL
);


--
-- TOC entry 248 (class 1259 OID 67235)
-- Name: mobile_device_usage_usage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.mobile_device_usage ALTER COLUMN usage_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mobile_device_usage_usage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 300 (class 1259 OID 67790)
-- Name: music; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.music (
    music_id integer NOT NULL,
    name character varying(200) NOT NULL,
    description text NOT NULL,
    link character varying(500),
    artist character varying(200) NOT NULL,
    duration interval,
    genre character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    created_by integer,
    updated_by integer,
    music_file character varying(100)
);


--
-- TOC entry 299 (class 1259 OID 67789)
-- Name: music_music_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.music ALTER COLUMN music_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.music_music_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 302 (class 1259 OID 67798)
-- Name: music_plays; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.music_plays (
    play_id integer NOT NULL,
    played_at timestamp with time zone NOT NULL,
    ip_address inet,
    user_agent text NOT NULL,
    session_duration interval,
    music_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- TOC entry 301 (class 1259 OID 67797)
-- Name: music_plays_play_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.music_plays ALTER COLUMN play_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.music_plays_play_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 261 (class 1259 OID 67308)
-- Name: operational_statuses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.operational_statuses (
    operational_status_id integer NOT NULL,
    status_name character varying(50) NOT NULL,
    description character varying(255) NOT NULL,
    sort_order integer NOT NULL
);


--
-- TOC entry 260 (class 1259 OID 67307)
-- Name: operational_statuses_operational_status_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.operational_statuses ALTER COLUMN operational_status_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.operational_statuses_operational_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 263 (class 1259 OID 67316)
-- Name: owner_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.owner_types (
    owner_type_id integer NOT NULL,
    type_name character varying(50) NOT NULL,
    description character varying(255) NOT NULL
);


--
-- TOC entry 262 (class 1259 OID 67315)
-- Name: owner_types_owner_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.owner_types ALTER COLUMN owner_type_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.owner_types_owner_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 226 (class 1259 OID 67020)
-- Name: permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions (
    permission_id integer NOT NULL,
    permission_name character varying(100) NOT NULL,
    resource_name character varying(50) NOT NULL,
    action_name character varying(20) NOT NULL,
    description character varying(255) NOT NULL
);


--
-- TOC entry 225 (class 1259 OID 67019)
-- Name: permissions_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.permissions ALTER COLUMN permission_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.permissions_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 241 (class 1259 OID 67087)
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role_permissions (
    id bigint NOT NULL,
    granted_at timestamp with time zone NOT NULL,
    granted_by integer NOT NULL,
    permission_id integer NOT NULL,
    role_id integer NOT NULL
);


--
-- TOC entry 240 (class 1259 OID 67086)
-- Name: role_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.role_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.role_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 265 (class 1259 OID 67324)
-- Name: service_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.service_categories (
    service_category_id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    description character varying(500) NOT NULL,
    icon_url character varying(500) NOT NULL
);


--
-- TOC entry 264 (class 1259 OID 67323)
-- Name: service_categories_service_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.service_categories ALTER COLUMN service_category_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.service_categories_service_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 237 (class 1259 OID 67069)
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_profiles (
    profile_id integer NOT NULL,
    avatar_url character varying(500) NOT NULL,
    bio text NOT NULL,
    department character varying(100) NOT NULL,
    job_title character varying(100) NOT NULL,
    notification_preferences jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    user_id integer NOT NULL
);


--
-- TOC entry 236 (class 1259 OID 67068)
-- Name: user_profiles_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.user_profiles ALTER COLUMN profile_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.user_profiles_profile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 243 (class 1259 OID 67093)
-- Name: user_role_assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_role_assignments (
    id bigint NOT NULL,
    assigned_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone,
    assigned_by integer NOT NULL,
    role_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- TOC entry 242 (class 1259 OID 67092)
-- Name: user_role_assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.user_role_assignments ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.user_role_assignments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 228 (class 1259 OID 67028)
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    description character varying(255) NOT NULL,
    is_system_role boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- TOC entry 227 (class 1259 OID 67027)
-- Name: user_roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.user_roles ALTER COLUMN role_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.user_roles_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 244 (class 1259 OID 67098)
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_sessions (
    session_id character varying(128) NOT NULL,
    ip_address inet,
    latitude numeric(10,8),
    longitude numeric(11,8),
    session_data jsonb NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    last_activity_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    ended_at timestamp with time zone,
    user_id integer NOT NULL,
    game_high_score integer NOT NULL
);


--
-- TOC entry 230 (class 1259 OID 67036)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    password character varying(128) NOT NULL,
    user_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    phone_number character varying(20) NOT NULL,
    is_active boolean NOT NULL,
    verified boolean NOT NULL,
    password_reset_token character varying(255) NOT NULL,
    password_changed_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    is_staff boolean NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(150),
    last_login timestamp with time zone,
    date_joined timestamp with time zone NOT NULL
);


--
-- TOC entry 232 (class 1259 OID 67050)
-- Name: users_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- TOC entry 231 (class 1259 OID 67049)
-- Name: users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 229 (class 1259 OID 67035)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users ALTER COLUMN user_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 234 (class 1259 OID 67056)
-- Name: users_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- TOC entry 233 (class 1259 OID 67055)
-- Name: users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 271 (class 1259 OID 67367)
-- Name: wards; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.wards (
    ward_id integer NOT NULL,
    ward_name character varying(100) NOT NULL,
    ward_code character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    constituency_id integer NOT NULL
);


--
-- TOC entry 270 (class 1259 OID 67366)
-- Name: wards_ward_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.wards ALTER COLUMN ward_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.wards_ward_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4066 (class 0 OID 67079)
-- Dependencies: 239
-- Data for Name: api_tokens; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.api_tokens (token_id, token_name, token_hash, last_used_at, is_active, created_at, expires_at, user_id) FROM stdin;
\.


--
-- TOC entry 4114 (class 0 OID 67598)
-- Dependencies: 287
-- Data for Name: audit_trail; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.audit_trail (audit_id, table_name, record_id, action_type, event_category, ip_address, old_values, new_values, changed_fields, severity_level, description, justification, failure_reason, metadata, created_at, session_id) FROM stdin;
\.


--
-- TOC entry 4049 (class 0 OID 66980)
-- Dependencies: 222
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 4051 (class 0 OID 66988)
-- Dependencies: 224
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 4047 (class 0 OID 66974)
-- Dependencies: 220
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Token	6	add_token
22	Can change Token	6	change_token
23	Can delete Token	6	delete_token
24	Can view Token	6	view_token
25	Can add Token	7	add_tokenproxy
26	Can change Token	7	change_tokenproxy
27	Can delete Token	7	delete_tokenproxy
28	Can view Token	7	view_tokenproxy
33	Can add permission	9	add_permission
34	Can change permission	9	change_permission
35	Can delete permission	9	delete_permission
36	Can view permission	9	view_permission
29	Can add user role	8	add_userrole
30	Can change user role	8	change_userrole
31	Can delete user role	8	delete_userrole
32	Can view user role	8	view_userrole
41	Can add user	11	add_user
42	Can change user	11	change_user
43	Can delete user	11	delete_user
44	Can view user	11	view_user
61	Can add custom token	16	add_customtoken
62	Can change custom token	16	change_customtoken
63	Can delete custom token	16	delete_customtoken
64	Can view custom token	16	view_customtoken
49	Can add user profile	13	add_userprofile
50	Can change user profile	13	change_userprofile
51	Can delete user profile	13	delete_userprofile
52	Can view user profile	13	view_userprofile
57	Can add api token	15	add_apitoken
58	Can change api token	15	change_apitoken
59	Can delete api token	15	delete_apitoken
60	Can view api token	15	view_apitoken
37	Can add role permission	10	add_rolepermission
38	Can change role permission	10	change_rolepermission
39	Can delete role permission	10	delete_rolepermission
40	Can view role permission	10	view_rolepermission
45	Can add user role assignment	12	add_userroleassignment
46	Can change user role assignment	12	change_userroleassignment
47	Can delete user role assignment	12	delete_userroleassignment
48	Can view user role assignment	12	view_userroleassignment
53	Can add user session	14	add_usersession
54	Can change user session	14	change_usersession
55	Can delete user session	14	delete_usersession
56	Can view user session	14	view_usersession
65	Can add facility	17	add_facility
66	Can change facility	17	change_facility
67	Can delete facility	17	delete_facility
68	Can view facility	17	view_facility
69	Can add facility contact	18	add_facilitycontact
70	Can change facility contact	18	change_facilitycontact
71	Can delete facility contact	18	delete_facilitycontact
72	Can view facility contact	18	view_facilitycontact
73	Can add facility coordinate	19	add_facilitycoordinate
74	Can change facility coordinate	19	change_facilitycoordinate
75	Can delete facility coordinate	19	delete_facilitycoordinate
76	Can view facility coordinate	19	view_facilitycoordinate
89	Can add facility gbv category	23	add_facilitygbvcategory
90	Can change facility gbv category	23	change_facilitygbvcategory
91	Can delete facility gbv category	23	delete_facilitygbvcategory
92	Can view facility gbv category	23	view_facilitygbvcategory
81	Can add facility infrastructure	21	add_facilityinfrastructure
82	Can change facility infrastructure	21	change_facilityinfrastructure
83	Can delete facility infrastructure	21	delete_facilityinfrastructure
84	Can view facility infrastructure	21	view_facilityinfrastructure
85	Can add facility owner	22	add_facilityowner
86	Can change facility owner	22	change_facilityowner
87	Can delete facility owner	22	delete_facilityowner
88	Can view facility owner	22	view_facilityowner
77	Can add facility service	20	add_facilityservice
78	Can change facility service	20	change_facilityservice
79	Can delete facility service	20	delete_facilityservice
80	Can view facility service	20	view_facilityservice
93	Can add county	24	add_county
94	Can change county	24	change_county
95	Can delete county	24	delete_county
96	Can view county	24	view_county
97	Can add constituency	25	add_constituency
98	Can change constituency	25	change_constituency
99	Can delete constituency	25	delete_constituency
100	Can view constituency	25	view_constituency
101	Can add ward	26	add_ward
102	Can change ward	26	change_ward
103	Can delete ward	26	delete_ward
104	Can view ward	26	view_ward
129	Can add condition status	33	add_conditionstatus
130	Can change condition status	33	change_conditionstatus
131	Can delete condition status	33	delete_conditionstatus
132	Can view condition status	33	view_conditionstatus
109	Can add contact type	28	add_contacttype
110	Can change contact type	28	change_contacttype
111	Can delete contact type	28	delete_contacttype
112	Can view contact type	28	view_contacttype
133	Can add document type	34	add_documenttype
134	Can change document type	34	change_documenttype
135	Can delete document type	34	delete_documenttype
136	Can view document type	34	view_documenttype
121	Can add gbv category	31	add_gbvcategory
122	Can change gbv category	31	change_gbvcategory
123	Can delete gbv category	31	delete_gbvcategory
124	Can view gbv category	31	view_gbvcategory
125	Can add infrastructure type	32	add_infrastructuretype
126	Can change infrastructure type	32	change_infrastructuretype
127	Can delete infrastructure type	32	delete_infrastructuretype
128	Can view infrastructure type	32	view_infrastructuretype
105	Can add operational status	27	add_operationalstatus
106	Can change operational status	27	change_operationalstatus
107	Can delete operational status	27	delete_operationalstatus
108	Can view operational status	27	view_operationalstatus
117	Can add owner type	30	add_ownertype
118	Can change owner type	30	change_ownertype
119	Can delete owner type	30	delete_ownertype
120	Can view owner type	30	view_ownertype
113	Can add service category	29	add_servicecategory
114	Can change service category	29	change_servicecategory
115	Can delete service category	29	delete_servicecategory
116	Can view service category	29	view_servicecategory
137	Can add document	35	add_document
138	Can change document	35	change_document
139	Can delete document	35	delete_document
140	Can view document	35	view_document
145	Can add audit trail	37	add_audittrail
146	Can change audit trail	37	change_audittrail
147	Can delete audit trail	37	delete_audittrail
148	Can view audit trail	37	view_audittrail
141	Can add contact interaction	36	add_contactinteraction
142	Can change contact interaction	36	change_contactinteraction
143	Can delete contact interaction	36	delete_contactinteraction
144	Can view contact interaction	36	view_contactinteraction
149	Can add music	38	add_music
150	Can change music	38	change_music
151	Can delete music	38	delete_music
152	Can view music	38	view_music
153	Can add music play	39	add_musicplay
154	Can change music play	39	change_musicplay
155	Can delete music play	39	delete_musicplay
156	Can view music play	39	view_musicplay
157	Can add mobile session	40	add_mobilesession
158	Can change mobile session	40	change_mobilesession
159	Can delete mobile session	40	delete_mobilesession
160	Can view mobile session	40	view_mobilesession
161	Can add mobile app usage	41	add_mobileappusage
162	Can change mobile app usage	41	change_mobileappusage
163	Can delete mobile app usage	41	delete_mobileappusage
164	Can view mobile app usage	41	view_mobileappusage
165	Can add Conversation	42	add_conversation
166	Can change Conversation	42	change_conversation
167	Can delete Conversation	42	delete_conversation
168	Can view Conversation	42	view_conversation
169	Can add Message	43	add_message
170	Can change Message	43	change_message
171	Can delete Message	43	delete_message
172	Can view Message	43	view_message
173	Can add Chat Notification	44	add_chatnotification
174	Can change Chat Notification	44	change_chatnotification
175	Can delete Chat Notification	44	delete_chatnotification
176	Can view Chat Notification	44	view_chatnotification
\.


--
-- TOC entry 4117 (class 0 OID 67641)
-- Dependencies: 290
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
\.


--
-- TOC entry 4078 (class 0 OID 67262)
-- Dependencies: 251
-- Data for Name: condition_statuses; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.condition_statuses (condition_status_id, status_name, description) FROM stdin;
1	Excellent	In excellent condition
2	Good	In good condition
3	Fair	In fair condition
4	Poor	In poor condition
5	Critical	In critical condition requiring immediate attention
6	Under Maintenance	Currently under maintenance
7	Out of Service	Currently out of service
8	Unknown	Condition unknown
\.


--
-- TOC entry 4096 (class 0 OID 67359)
-- Dependencies: 269
-- Data for Name: constituencies; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.constituencies (constituency_id, constituency_name, constituency_code, created_at, updated_at, county_id) FROM stdin;
127	Baringo Central	58B294CD	2025-09-01 19:56:33.879+03	2025-09-01 19:56:33.879+03	87
128	Eldama Ravine	0457908B	2025-09-01 19:56:35.24+03	2025-09-01 19:56:35.24+03	87
129	Eldoret East	A11BDB86	2025-09-01 19:56:37.409+03	2025-09-01 19:56:37.409+03	88
130	Westlands	4ABCC6FB	2025-09-01 19:56:37.444+03	2025-09-01 19:56:37.444+03	89
131	Nakuru Central	593CD628	2025-09-01 19:56:37.485+03	2025-09-01 19:56:37.485+03	90
132	Bomet Central	85B6B21C	2025-09-01 19:56:37.552+03	2025-09-01 19:56:37.552+03	91
133	Kericho Central	AFF5BFAB	2025-09-01 19:56:37.599+03	2025-09-01 19:56:37.599+03	92
134	Kisumu Central	04BE434D	2025-09-01 19:56:37.64+03	2025-09-01 19:56:37.64+03	93
135	Bungoma Central	A12299E5	2025-09-01 19:56:37.756+03	2025-09-01 19:56:37.756+03	94
136	Kakamega Central	64C5CC9F	2025-09-01 19:57:47.72+03	2025-09-01 19:57:47.72+03	95
137	Migori Central	35CC9430	2025-09-01 19:58:05.861+03	2025-09-01 19:58:05.861+03	96
138	Busia Central	36C84A04	2025-09-01 19:58:43.599+03	2025-09-01 19:58:43.599+03	97
139	Siaya Central	C6B88FBE	2025-09-01 19:59:19.606+03	2025-09-01 19:59:19.606+03	98
140	Embu Central	200EF7FD	2025-09-01 19:59:57.069+03	2025-09-01 19:59:57.069+03	99
141	Meru Central	486B845A	2025-09-01 20:00:24.349+03	2025-09-01 20:00:24.349+03	100
142	Garissa Central	497DA460	2025-09-01 20:01:51.292+03	2025-09-01 20:01:51.292+03	101
143	Kisii Central	F304A772	2025-09-01 20:03:31.68+03	2025-09-01 20:03:31.68+03	102
144	Mombasa Central	57045135	2025-09-01 20:03:46.302+03	2025-09-01 20:03:46.302+03	103
145	Isiolo Central	24117760	2025-09-01 20:04:02.655+03	2025-09-01 20:04:02.655+03	104
\.


--
-- TOC entry 4116 (class 0 OID 67606)
-- Dependencies: 289
-- Data for Name: contact_interactions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contact_interactions (interaction_id, user_latitude, user_longitude, is_helpful, created_at, contact_id, device_id, click_data, interaction_type) FROM stdin;
\.


--
-- TOC entry 4080 (class 0 OID 67270)
-- Dependencies: 253
-- Data for Name: contact_types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contact_types (contact_type_id, type_name, validation_regex) FROM stdin;
1	Phone	
2	Email	
3	Emergency Contact	
4	WhatsApp	
5	Primary Contact	
6	Manager	
7	Director	
8	Supervisor	
9	Staff	
10	Administrative Contact	
11	Mobile	^\\+?[0-9\\s\\-\\(\\)]+$
12	Fax	^\\+?[0-9\\s\\-\\(\\)]+$
13	Website	^https?://[^\\s/$.?#].[^\\s]*$
14	Physical Address	
15	Postal Address	
\.


--
-- TOC entry 4094 (class 0 OID 67351)
-- Dependencies: 267
-- Data for Name: counties; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.counties (county_id, county_name, county_code, created_at, updated_at) FROM stdin;
87	Baringo	D8239B0E	2025-09-01 19:56:33.866+03	2025-09-01 19:56:33.866+03
88	Eldoret	BB376E64	2025-09-01 19:56:37.4+03	2025-09-01 19:56:37.4+03
89	Nairobi	FC938980	2025-09-01 19:56:37.435+03	2025-09-01 19:56:37.435+03
90	Nakuru	19C534B0	2025-09-01 19:56:37.476+03	2025-09-01 19:56:37.476+03
91	Bomet	C29FB2EB	2025-09-01 19:56:37.542+03	2025-09-01 19:56:37.542+03
92	Kericho	6986327C	2025-09-01 19:56:37.589+03	2025-09-01 19:56:37.589+03
93	Kisumu	0180158F	2025-09-01 19:56:37.627+03	2025-09-01 19:56:37.627+03
94	Bungoma	77172FE5	2025-09-01 19:56:37.738+03	2025-09-01 19:56:37.738+03
95	Kakamega	12EB2A81	2025-09-01 19:57:47.706+03	2025-09-01 19:57:47.706+03
96	Migori	17BF2105	2025-09-01 19:58:05.855+03	2025-09-01 19:58:05.855+03
97	Busia	E9F0E3F9	2025-09-01 19:58:43.592+03	2025-09-01 19:58:43.592+03
98	Siaya	0EFB3FD1	2025-09-01 19:59:19.6+03	2025-09-01 19:59:19.6+03
99	Embu	DEA987BD	2025-09-01 19:59:57.062+03	2025-09-01 19:59:57.062+03
100	Meru	DBAB04EE	2025-09-01 20:00:24.337+03	2025-09-01 20:00:24.337+03
101	Garissa	05FC8129	2025-09-01 20:01:51.284+03	2025-09-01 20:01:51.284+03
102	Kisii	6D353F61	2025-09-01 20:03:31.673+03	2025-09-01 20:03:31.673+03
103	Mombasa	DCE6433A	2025-09-01 20:03:46.294+03	2025-09-01 20:03:46.294+03
104	Isiolo	302BDDA4	2025-09-01 20:04:02.633+03	2025-09-01 20:04:02.633+03
\.


--
-- TOC entry 4062 (class 0 OID 67061)
-- Dependencies: 235
-- Data for Name: custom_tokens; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.custom_tokens (key, created, user_id) FROM stdin;
\.


--
-- TOC entry 4073 (class 0 OID 67210)
-- Dependencies: 246
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 4045 (class 0 OID 66966)
-- Dependencies: 218
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	authtoken	token
7	authtoken	tokenproxy
9	authentication	permission
8	authentication	userrole
11	authentication	user
16	authentication	customtoken
13	authentication	userprofile
15	authentication	apitoken
10	authentication	rolepermission
12	authentication	userroleassignment
14	authentication	usersession
17	facilities	facility
18	facilities	facilitycontact
19	facilities	facilitycoordinate
23	facilities	facilitygbvcategory
21	facilities	facilityinfrastructure
22	facilities	facilityowner
20	facilities	facilityservice
24	geography	county
25	geography	constituency
26	geography	ward
33	lookups	conditionstatus
28	lookups	contacttype
34	lookups	documenttype
31	lookups	gbvcategory
32	lookups	infrastructuretype
27	lookups	operationalstatus
30	lookups	ownertype
29	lookups	servicecategory
35	documents	document
37	analytics	audittrail
36	analytics	contactinteraction
38	music	music
39	music	musicplay
40	mobile_sessions	mobilesession
41	mobile_sessions	mobileappusage
42	chat	conversation
43	chat	message
44	chat	chatnotification
\.


--
-- TOC entry 4043 (class 0 OID 66958)
-- Dependencies: 216
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-09-03 11:46:52.651929+03
2	contenttypes	0002_remove_content_type_name	2025-09-03 11:46:52.665026+03
3	auth	0001_initial	2025-09-03 11:46:52.737642+03
4	auth	0002_alter_permission_name_max_length	2025-09-03 11:46:52.745579+03
5	auth	0003_alter_user_email_max_length	2025-09-03 11:46:52.7558+03
6	auth	0004_alter_user_username_opts	2025-09-03 11:46:52.767041+03
7	auth	0005_alter_user_last_login_null	2025-09-03 11:46:52.775919+03
8	auth	0006_require_contenttypes_0002	2025-09-03 11:46:52.78408+03
9	auth	0007_alter_validators_add_error_messages	2025-09-03 11:46:52.800742+03
10	auth	0008_alter_user_username_max_length	2025-09-03 11:46:52.809114+03
11	auth	0009_alter_user_last_name_max_length	2025-09-03 11:46:52.818268+03
12	auth	0010_alter_group_name_max_length	2025-09-03 11:46:52.829802+03
13	auth	0011_update_proxy_permissions	2025-09-03 11:46:52.841294+03
14	auth	0012_alter_user_first_name_max_length	2025-09-03 11:46:52.854438+03
15	authentication	0001_initial	2025-09-03 11:46:53.283879+03
16	admin	0001_initial	2025-09-03 11:46:53.340231+03
17	admin	0002_logentry_remove_auto_add	2025-09-03 11:46:53.368974+03
18	admin	0003_logentry_add_action_flag_choices	2025-09-03 11:46:53.385265+03
19	mobile_sessions	0001_initial	2025-09-03 11:46:53.52181+03
20	mobile_sessions	0002_rename_mobile_dev_session_456def_idx_mobile_devi_device__b7f94d_idx_and_more	2025-09-03 11:46:53.569068+03
21	lookups	0001_initial	2025-09-03 11:46:53.980496+03
22	geography	0001_initial	2025-09-03 11:46:54.279039+03
23	facilities	0001_initial	2025-09-03 11:46:55.46858+03
24	analytics	0001_initial	2025-09-03 11:46:55.774273+03
25	analytics	0003_alter_contactinteraction_device	2025-09-03 11:46:55.828486+03
26	analytics	0004_alter_contactinteraction_device	2025-09-03 11:46:55.909816+03
27	analytics	0005_contactinteraction_click_data_and_more	2025-09-03 11:46:55.947615+03
28	authentication	0002_remove_user_password_hash	2025-09-03 11:46:55.989225+03
29	authentication	0003_usersession_game_high_score	2025-09-03 11:46:56.032799+03
30	authentication	0004_alter_userprofile_avatar_url	2025-09-03 11:46:56.070522+03
31	authtoken	0001_initial	2025-09-03 11:46:56.165865+03
32	authtoken	0002_auto_20160226_1747	2025-09-03 11:46:56.31019+03
33	authtoken	0003_tokenproxy	2025-09-03 11:46:56.324515+03
34	authtoken	0004_alter_tokenproxy_options	2025-09-03 11:46:56.336336+03
35	mobile_sessions	0003_mobilesession_game_high_score	2025-09-03 11:46:56.348012+03
36	chat	0001_initial	2025-09-03 11:46:57.388438+03
37	chat	0002_alter_message_media_url	2025-09-03 11:46:57.428927+03
38	chat	0003_alter_message_media_file	2025-09-03 11:46:57.479979+03
39	documents	0001_initial	2025-09-03 11:46:57.640353+03
40	documents	0002_document_file	2025-09-03 11:46:57.689925+03
41	lookups	0002_gbvcategory_icon_url_servicecategory_icon_url	2025-09-03 11:46:57.724621+03
42	facilities	0002_facilityinfrastructure_created_by_and_more	2025-09-03 11:46:57.965856+03
43	music	0001_initial	2025-09-03 11:46:58.551112+03
44	music	0002_alter_music_created_by	2025-09-03 11:46:58.818543+03
45	music	0003_add_music_file_field	2025-09-03 11:46:58.917547+03
46	sessions	0001_initial	2025-09-03 11:46:58.965283+03
\.


--
-- TOC entry 4130 (class 0 OID 67840)
-- Dependencies: 303
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
53o3xwls2wd41wvcrrkuafvdos6qfv0g	.eJxVjsuqwkAQRP9l1hoyk2kz49IHKqh4xccydGY6Jojx0Ql6Ef_diC50W4c6VXeRYF3lSc10SQovukKK1neWottT-QJ4OnHwAlRWhcOqOJbBh3LQr7k6HtZNo_cp_Fhy5LxRaC0NZLEyYSSVt6DIUaZdliJhpL21xmgLkQxV5pwycUdTB0wMBoxVWmEjZWJult9fNyX-E1wXhfeL4Szehucxy8Fyd4HRHNupSlcwvfnzJEz-xOMJy9dMoA:1ut8dB:5PZp9-yfqEz6J8bWGnwLJViN8nCqfCpZyg87b_fmdPU	2025-09-02 20:47:49.126+03
khdpszhft5mf93ecc61yfoeysfoibxig	.eJxVjssOgjAURP-la0OgtNC6lIUG48bImlzaS0HloaUhwfjvQmSh2zmZM_MiObihyp3FZ15rsiUB2fxmBagbtguAvrfeArAdagVD3bXeSq2XODt0TTY3dmvhz1KBrWYFY4HgZUyFHwZUS05RYclUWQBCyLSUQjDJw8CnpVJUxBHDiIuYCy4kZRRmqUVr5-XvV-1OqI_3XnOTpm40IYUmMdPUaX4-5FGye1yya8Zqsx_J-wPfYU2Q:1urzJd:P3hEQDKPCAnTu1A-WL6zo37FJPM77FjXAlx_cfGR6vg	2025-08-30 16:38:53.337+03
\.


--
-- TOC entry 4082 (class 0 OID 67278)
-- Dependencies: 255
-- Data for Name: document_types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.document_types (document_type_id, type_name, allowed_extensions, max_file_size_mb, description) FROM stdin;
1	Policy Document		10	Official policy or procedure documents
2	Training Material		10	Training guides, manuals, or educational materials
3	Report		10	Incident reports, case studies, or research reports
4	Form		10	Official forms, applications, or templates
5	Reference Material		10	Reference guides, directories, or informational materials
\.


--
-- TOC entry 4125 (class 0 OID 67744)
-- Dependencies: 298
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.documents (document_id, title, description, file_url, file_name, file_size_bytes, content, image_url, external_url, is_public, is_active, uploaded_at, document_type_id, gbv_category, uploaded_by, file) FROM stdin;
\.


--
-- TOC entry 4119 (class 0 OID 67656)
-- Dependencies: 292
-- Data for Name: emergency_chat_conversations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.emergency_chat_conversations (conversation_id, status, priority, subject, last_message, last_message_at, unread_count_mobile, unread_count_admin, created_at, updated_at, assigned_admin_id, last_message_by_id, mobile_session_id) FROM stdin;
\.


--
-- TOC entry 4121 (class 0 OID 67664)
-- Dependencies: 294
-- Data for Name: emergency_chat_messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.emergency_chat_messages (message_id, sender_type, content, message_type, media_file, media_url, status, sent_at, delivered_at, read_at, is_urgent, metadata, conversation_id, sender_id) FROM stdin;
\.


--
-- TOC entry 4123 (class 0 OID 67672)
-- Dependencies: 296
-- Data for Name: emergency_chat_notifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.emergency_chat_notifications (notification_id, notification_type, title, body, is_read, created_at, user_id, conversation_id, message_id) FROM stdin;
\.


--
-- TOC entry 4100 (class 0 OID 67398)
-- Dependencies: 273
-- Data for Name: facilities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facilities (facility_id, facility_name, facility_code, registration_number, address_line_1, address_line_2, is_active, description, website_url, created_at, updated_at, created_by, operational_status_id, updated_by, ward_id) FROM stdin;
12201	Baringo County Referral Hospital	BARINGOCOU-BAR-0E0087	2GK-004476		P.O BOX 21-30400 KABARNET HOSPITAL LEVEL 4 Public LEVEL 4 100 BARINGO LICENCED	t			2025-09-01 19:56:33.893+03	2025-09-01 19:56:33.893+03	2	1	\N	191
12202	Eldama Ra Vine Sub-County Hospital	ELDAMARAVI-BAR-5017D5	3GK-013469		P.O BOX 102-20103 ELDAMA RA VINE HOSPITAL LEVEL 4 Public LEVEL 4 120 BARINGO LICENCED	t			2025-09-01 19:56:35.252+03	2025-09-01 19:56:35.252+03	2	1	\N	192
12203	Mercy Mission Hospital	MERCYMISSI-BAR-B55982			P.O BOX 10-20103 ELDAMA RA VINE FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 110 BARINGO LICENCED	t			2025-09-01 19:56:37.316+03	2025-09-01 19:56:37.316+03	2	1	\N	192
12204	Kitabisi Dispensary	KITABISIDI-BUN-33F192	98GK-012151		P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:37.771+03	2025-09-01 19:56:37.771+03	2	1	\N	199
12205	Kibuke Health Centre	KIBUKEHEAL-BUN-6F7B47	GK-012387		P.O BOX 14-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 18BUNGOMA LICENCED	t			2025-09-01 19:56:39.03+03	2025-09-01 19:56:39.03+03	2	1	\N	199
12206	Muanda Health Centre	MUANDAHEAL-BUN-0436AF	GK-012442		P.O BOX 754-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 21BUNGOMA LICENCED	t			2025-09-01 19:56:39.087+03	2025-09-01 19:56:39.087+03	2	1	\N	199
12207	Nasianda Health Centre	NASIANDAHE-BUN-267C88	GK-012448		P.O BOX 633-50200 BUNGOMA MEDICAL CLINIC Public LEVEL 2 6BUNGOMA LICENCED	t			2025-09-01 19:56:40.437+03	2025-09-01 19:56:40.437+03	2	1	\N	199
12208	Ranje Dispensary	RANJEDISPE-BUN-EAA5A6	GK-012544		P.O BOX 2495-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:40.535+03	2025-09-01 19:56:40.536+03	2	1	\N	199
12209	Kabula Health Centre	KABULAHEAL-BUN-133D2C	GK-012559		P.O BOX 14-50200 BUNGOMA HEALTH CENTRE Public LEVEL 3B 36BUNGOMA LICENCED	t			2025-09-01 19:56:40.61+03	2025-09-01 19:56:40.61+03	2	1	\N	199
12210	Bukokholo Dispensary	BUKOKHOLOD-BUN-8BF7D6	GK-012685		P.O BOX 182-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:40.666+03	2025-09-01 19:56:40.666+03	2	1	\N	199
12211	Bungoma G.K Prison Health Centre	BUNGOMAGKP-BUN-987C67	GK-012722		P.O BOX 56-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 26BUNGOMA LICENCED	t			2025-09-01 19:56:41.863+03	2025-09-01 19:56:41.863+03	2	1	\N	199
12212	Mayanja Health Centre	MAYANJAHEA-BUN-9F0AA1	GK-012727		P.O BOX 101-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 17BUNGOMA LICENCED	t			2025-09-01 19:56:43.368+03	2025-09-01 19:56:43.368+03	2	1	\N	199
12213	Webuye Sub-County Hospital	WEBUYESUBC-BUN-D45B04	GK-012892		P.O BOX 25-50205 WEBUYE HOSPITAL LEVEL 4 Public LEVEL 4 217 BUNGOMA LICENCED	t			2025-09-01 19:56:43.425+03	2025-09-01 19:56:43.425+03	2	1	\N	199
12214	Bungoma County Referral Hospital	BUNGOMACOU-BUN-9C0075	GK-012982		P.O BOX 14-50200 BUNGOMA HOSPITAL LEVEL 5 Public LEVEL 5 565 BUNGOMA LICENCED	t			2025-09-01 19:56:44.71+03	2025-09-01 19:56:44.71+03	2	1	\N	199
12215	Bumula Sub-County Hospital	BUMULASUBC-BUN-D6AED0	GK-012998		P.O BOX 14-50200 BUNGOMA HOSPITAL LEVEL 4 Public LEVEL 4 30BUNGOMA LICENCED	t			2025-09-01 19:56:46.305+03	2025-09-01 19:56:46.305+03	2	1	\N	199
12216	Kimilili Sub-County Hospital	KIMILILISU-BUN-0979ED	GK-013006		P.O BOX 490-50204 KIMILILI HOSPITAL LEVEL 4 Public LEVEL 4 180 BUNGOMA LICENCED	t			2025-09-01 19:56:47.719+03	2025-09-01 19:56:47.719+03	2	1	\N	199
12217	Kimaeti Health Centre	KIMAETIHEA-BUN-CFBF28	GK-013046		P.O BOX 2313-50200 BUNGOMA HEALTH CENTRE Public LEVEL 3B 35BUNGOMA LICENCED	t			2025-09-01 19:56:49.383+03	2025-09-01 19:56:49.383+03	2	1	\N	199
12218	Mechimeru Health Centre	MECHIMERUH-BUN-872B6D	GK-013116		P.O BOX 14-50200 BUNGOMA HEALTH CENTRE Public LEVEL 3B 6BUNGOMA LICENCED	t			2025-09-01 19:56:49.454+03	2025-09-01 19:56:49.454+03	2	1	\N	199
12219	Bukembe Health Centre	BUKEMBEHEA-BUN-0FA1A6	GK-013210		P.O BOX 14-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 20BUNGOMA LICENCED	t			2025-09-01 19:56:49.518+03	2025-09-01 19:56:49.518+03	2	1	\N	199
12220	Bisunu Dispensary	BISUNUDISP-BUN-935AA5	GK-018717		P.O BOX 768-50200 BUNGOMA DISPENSARY Public LEVEL 2 5BUNGOMA LICENCED	t			2025-09-01 19:56:49.579+03	2025-09-01 19:56:49.579+03	2	1	\N	199
12221	Tulienge Dispensary	TULIENGEDI-BUN-FA22FF	GK-019056		P.O BOX 122-50208 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:50.719+03	2025-09-01 19:56:50.719+03	2	1	\N	199
12222	Bulondo Health Centre	BULONDOHEA-BUN-FAE8FF	GK-020695		P.O BOX 14-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 25BUNGOMA LICENCED	t			2025-09-01 19:56:52.006+03	2025-09-01 19:56:52.006+03	2	1	\N	199
12223	Nabukhisa Dispensary	NABUKHISAD-BUN-89C0B0	GK-020696		P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:52.071+03	2025-09-01 19:56:52.071+03	2	1	\N	199
12224	Myanga Health Centre	MYANGAHEAL-BUN-233C77	GK-020697		P.O BOX 23194-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 15BUNGOMA LICENCED	t			2025-09-01 19:56:53.322+03	2025-09-01 19:56:53.322+03	2	1	\N	199
12225	Kamusinde Dispensary	KAMUSINDED-BUN-739AA2	GK-020699		P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:55.02+03	2025-09-01 19:56:55.02+03	2	1	\N	199
12226	Kisawaiyi Dispensary	KISAWAIYID-BUN-476F8F	GK-020701		P.O BOX 437-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:56.24+03	2025-09-01 19:56:56.24+03	2	1	\N	199
12227	Kipsabula Dispensary	KIPSABULAD-BUN-8A7B2C	GK-020706		P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:57.459+03	2025-09-01 19:56:57.459+03	2	1	\N	199
12228	Samoya Dispensary	SAMOYADISP-BUN-82A8F5	GK-020714		P.O BOX 1835-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:58.7+03	2025-09-01 19:56:58.7+03	2	1	\N	199
12229	Butieli Dispensary	BUTIELIDIS-BUN-7BF9B3	GK-020715		P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:56:59.793+03	2025-09-01 19:56:59.793+03	2	1	\N	199
12230	Siritanyi Health Centre	SIRITANYIH-BUN-6CD679	GK-020717		P.O BOX 437-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 14BUNGOMA LICENCED	t			2025-09-01 19:57:01.309+03	2025-09-01 19:57:01.309+03	2	1	\N	199
12231	Kongit Dispensary	KONGITDISP-BUN-A162B2	GK-020724		P.O BOX 49-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:02.579+03	2025-09-01 19:57:02.579+03	2	1	\N	199
12232	Makololwe Dispensary	MAKOLOLWED-BUN-3E14DA	GK-020725		P.O BOX 49-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:04.317+03	2025-09-01 19:57:04.317+03	2	1	\N	199
12233	Makunga Dispensary	MAKUNGADIS-BUN-292983	GK-020728		P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:05.945+03	2025-09-01 19:57:05.945+03	2	1	\N	199
12234	Namirembe Dispensary	NAMIREMBED-BUN-2952C3	GK-020738		P.O BOX 170-50200 BUNGOMA DISPENSARY Public LEVEL 2 6BUNGOMA LICENCED	t			2025-09-01 19:57:07.857+03	2025-09-01 19:57:07.857+03	2	1	\N	199
12235	Fathers Love Foundation Clinic	FATHERSLOV-BUN-15B99E	000847		P.O BOX 1202-50200 BUNGOMA DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:09.059+03	2025-09-01 19:57:09.059+03	2	1	\N	199
12236	Mission Of Mercy Hospital	MISSIONOFM-BUN-BF9FEF	001312		P.O BOX 1429-50200 BUNGOMA MISSION HOSPITAL LEVEL 3 FAITH BASED ORGANIZATION (FBO) LEVEL 3A 35BUNGOMA LICENCED	t			2025-09-01 19:57:10.526+03	2025-09-01 19:57:10.526+03	2	1	\N	199
12237	St Anthonys Kibabii Health Centre	STANTHONYS-BUN-30E649	004329		P.O BOX 512-5200 BUNGOMA HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 24BUNGOMA LICENCED	t			2025-09-01 19:57:10.598+03	2025-09-01 19:57:10.598+03	2	1	\N	199
12238	St. Damiano Mission Hospital	STDAMIANOM-BUN-61CF20	006761		P.O BOX 1769-50200 BUNGOMA FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 80BUNGOMA LICENCED	t			2025-09-01 19:57:12.204+03	2025-09-01 19:57:12.204+03	2	1	\N	199
12239	Ack Dr. Pike Roper Medical Centre	ACKDRPIKER-BUN-94E0DE	016033		P.O BOX 2392-50200 BUNGOMA FAITH-BASED BASIC CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3A 0BUNGOMA LICENCED	t			2025-09-01 19:57:13.75+03	2025-09-01 19:57:13.75+03	2	1	\N	199
12240	Carmel Dispensary Kimwanga	CARMELDISP-BUN-EFB9CF	017966		P.O BOX 1658-50200 BUNGOMA DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:15.272+03	2025-09-01 19:57:15.272+03	2	1	\N	199
12241	New Elgon View Medical Cottage	NEWELGONVI-BUN-7F5DDB	000475		P.O BOX 1747-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 64BUNGOMA LICENCED	t			2025-09-01 19:57:16.728+03	2025-09-01 19:57:16.728+03	2	1	\N	199
12242	Machwele Friends Dispensary	MACHWELEFR-BUN-202314	000640		P.O BOX 1463-50200 BUNGOMA FAITH BASED DISPENSARY Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:18.857+03	2025-09-01 19:57:18.857+03	2	1	\N	199
12243	Nzoia Medical Centre	NZOIAMEDIC-BUN-2249E6	002868		P.O BOX 471-50200 BUNGOMA NURSING HOME Private LEVEL 3B 75BUNGOMA LICENCED	t			2025-09-01 19:57:20.557+03	2025-09-01 19:57:20.557+03	2	1	\N	199
12244	The Aga Khan Hospital Bungoma	THEAGAKHAN-KIS-5B691F	003268		P.O BOX 530-40100 KISUMU MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED	t			2025-09-01 19:57:20.636+03	2025-09-01 19:57:20.636+03	2	1	\N	198
12245	Bungoma West Hospital	BUNGOMAWES-BUN-704574	003310		P.O BOX 152-50200 BUNGOMA HOSPITAL LEVEL 5 Private LEVEL 5 122 BUNGOMA LICENCED	t			2025-09-01 19:57:22.038+03	2025-09-01 19:57:22.038+03	2	1	\N	199
12246	Khalaba Medical Services	KHALABAMED-BUN-ABE5A4	003875		P.O BOX 2211-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 27BUNGOMA LICENCED	t			2025-09-01 19:57:23.744+03	2025-09-01 19:57:23.744+03	2	1	\N	199
12247	Bungoma Wema Centre	BUNGOMAWEM-BUN-7640FC	005031		P.O BOX 2270-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:23.809+03	2025-09-01 19:57:23.809+03	2	1	\N	199
12248	St. James Opticals	STJAMESOPT-BUN-DEC604	006269		P.O BOX 2141-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:25.151+03	2025-09-01 19:57:25.151+03	2	1	\N	199
12249	Kanduyi Health Centre	KANDUYIHEA-BUN-20B457	006351		P.O BOX 536-50200 BUNGOMA HEALTH CENTRE Private LEVEL 3B 0BUNGOMA LICENCED	t			2025-09-01 19:57:26.461+03	2025-09-01 19:57:26.461+03	2	1	\N	199
12250	Trinity Opticals Ltd	TRINITYOPT-BUN-2AA3D8	006504		P.O BOX 2397-50200 BUNGOMA EYE CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:28.14+03	2025-09-01 19:57:28.14+03	2	1	\N	199
12251	Bliss Healthcare Limited Kimilili	BLISSHEALT-NAI-23C204	006914		P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:29.724+03	2025-09-01 19:57:29.724+03	2	1	\N	194
12252	Bliss Healthcare Ltd Webuye	BLISSHEALT-NAI-19EC0D	007125		P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:31.167+03	2025-09-01 19:57:31.167+03	2	1	\N	194
12253	Nabuala Hospital	NABUALAHOS-BUN-65FF27	007256		P.O BOX 1001-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 120 BUNGOMA LICENCED	t			2025-09-01 19:57:32.558+03	2025-09-01 19:57:32.558+03	2	1	\N	199
12254	Fountain Healthcare Ltd Bungoma	FOUNTAINHE-BUN-075356	007319		P.O BOX 1596-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 26BUNGOMA LICENCED	t			2025-09-01 19:57:33.617+03	2025-09-01 19:57:33.617+03	2	1	\N	199
12255	Mpeli Medical Centre	MPELIMEDIC-BUN-E564C7	007913		P.O BOX 1699-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 30BUNGOMA LICENCED	t			2025-09-01 19:57:35.183+03	2025-09-01 19:57:35.183+03	2	1	\N	199
12256	Lifecare Hospitals Bungoma Ltd	LIFECAREHO-NAI-9E89C0	007994		P.O BOX 22476-00505 NAIROBI Hospital Level 5 Private LEVEL 5 105 BUNGOMA LICENCED	t			2025-09-01 19:57:36.15+03	2025-09-01 19:57:36.15+03	2	1	\N	194
12257	Zion Medical Centre - Bungoma Limited	ZIONMEDICA-BUN-3FB41A	008638		P.O BOX 1561-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 61BUNGOMA LICENCED	t			2025-09-01 19:57:37.84+03	2025-09-01 19:57:37.84+03	2	1	\N	199
12258	Kory Family Hospital Kimilili	KORYFAMILY-BUN-463549	014974		P.O BOX 1977-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 74BUNGOMA LICENCED	t			2025-09-01 19:57:39.203+03	2025-09-01 19:57:39.203+03	2	1	\N	199
12259	Bungoma West Hospital Town Annex Branch	BUNGOMAWES-BUN-FDABF2	015015		P.O BOX 152-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:40.887+03	2025-09-01 19:57:40.887+03	2	1	\N	199
12260	Brillian Doctors Plaza Hospital	BRILLIANDO-ELD-14DAB9	015233		P.O BOX 5881-30100 ELDORET NURSING HOME Private LEVEL 3B 25BUNGOMA LICENCED	t			2025-09-01 19:57:43.052+03	2025-09-01 19:57:43.052+03	2	1	\N	193
12261	Mercal Healthcare Bukembe	MERCALHEAL-BUN-BAD99D	015603		P.O BOX 244-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:44.615+03	2025-09-01 19:57:44.615+03	2	1	\N	199
12262	The Dawameds Hospital Limited	THEDAWAMED-BUN-7E1A5C	015642		P.O BOX 70-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 80BUNGOMA LICENCED	t			2025-09-01 19:57:46.095+03	2025-09-01 19:57:46.095+03	2	1	\N	199
12263	Chrizah Medical Clinic Limited	CHRIZAHMED-KAK-EF0DFB	015675		P.O BOX 911-50100 KAKAMEGA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:47.751+03	2025-09-01 19:57:47.751+03	2	1	\N	200
12264	Global Homecare Ltd Medical Centre	GLOBALHOME-BUN-AC7CCB	015751		P.O BOX 181-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:50.558+03	2025-09-01 19:57:50.558+03	2	1	\N	199
12265	Springwell Medical Clinic	SPRINGWELL-ELD-4355AE	015827		P.O BOX 4640-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:52.413+03	2025-09-01 19:57:52.413+03	2	1	\N	193
12266	Healridge Medical Centre	HEALRIDGEM-BUN-3EE205	015953		P.O BOX 552-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED	t			2025-09-01 19:57:54.212+03	2025-09-01 19:57:54.212+03	2	1	\N	199
12267	Mangs Health Care Clinic	MANGSHEALT-BUN-58CB0C	016211		P.O BOX 2212-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:57:55.517+03	2025-09-01 19:57:55.517+03	2	1	\N	199
12268	Wanda Medical Centre	WANDAMEDIC-BUN-69076B	016868		P.O BOX 1977-50200 BUNGOMA NURSING HOME Private LEVEL 3B 22BUNGOMA LICENCED	t			2025-09-01 19:57:57.221+03	2025-09-01 19:57:57.221+03	2	1	\N	199
12269	The Hopkins Crescent Hospitals Limited	THEHOPKINS-BUN-5AA898	016880		P.O BOX 2338-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 60BUNGOMA LICENCED	t			2025-09-01 19:57:58.436+03	2025-09-01 19:57:58.436+03	2	1	\N	199
12270	Bungoma Childrens Clinic Limited	BUNGOMACHI-ELD-BBF4B7	016979		P.O BOX 1125-30100 ELDORET MEDICAL CENTRE Private LEVEL 3A 10BUNGOMA LICENCED	t			2025-09-01 19:58:00.549+03	2025-09-01 19:58:00.549+03	2	1	\N	193
12271	Saint Jude Thaddeo Mabanga Clinic	SAINTJUDET-BUN-BE403D	017042		P.O BOX 997-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:02.35+03	2025-09-01 19:58:02.35+03	2	1	\N	199
12272	Buckner Family Hope Clinic	BUCKNERFAM-BUN-0DFF80	017065		P.O BOX 2520-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:03.998+03	2025-09-01 19:58:03.998+03	2	1	\N	199
12273	Oasis Doctors Plaza Webuye Limited	OASISDOCTO-MIG-6347DC	017319		P.O BOX 174-40400 MIGORI HOSPITAL LEVEL 4 Private LEVEL 4 45BUNGOMA LICENCED	t			2025-09-01 19:58:05.873+03	2025-09-01 19:58:05.873+03	2	1	\N	201
12274	The Dawameds Hospital Limited-Sirisia	THEDAWAMED-BUN-C1B2A4	018396		P.O BOX 2448-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 25BUNGOMA LICENCED	t			2025-09-01 19:58:07.608+03	2025-09-01 19:58:07.608+03	2	1	\N	199
12275	Bungoma Adorah Clinic	BUNGOMAADO-BUN-923557	018548		P.O BOX 15-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:09.167+03	2025-09-01 19:58:09.167+03	2	1	\N	199
12391	Odicare Medical Clinic	ODICAREMED-EMB-82F591	014772		P.O BOX 38- EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:35.439+03	2025-09-01 20:00:35.439+03	2	1	\N	204
12276	Afya Space Consultancy Ltd	AFYASPACEC-BUN-80B63C	018612		P.O BOX 545-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:10.812+03	2025-09-01 19:58:10.812+03	2	1	\N	199
12277	Rozajem Medical Centre	ROZAJEMMED-BUN-4BFAA9	019125		P.O BOX 352-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:12.749+03	2025-09-01 19:58:12.749+03	2	1	\N	199
12278	Al-Ihsaan Health Centre Kimaeti	ALIHSAANHE-BUN-E30382	019256		P.O BOX 11-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED	t			2025-09-01 19:58:14.069+03	2025-09-01 19:58:14.069+03	2	1	\N	199
12279	Connection Health Services Limited	CONNECTION-BUN-331488	019348		P.O BOX 14-50200 BUNGOMA NURSING HOME Private LEVEL 3B 36BUNGOMA LICENCED	t			2025-09-01 19:58:15.739+03	2025-09-01 19:58:15.739+03	2	1	\N	199
12280	St.Pauls Kibabii Ttc Medical Clinic	STPAULSKIB-BUN-C36192	019449		P.O BOX 931-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:17.36+03	2025-09-01 19:58:17.36+03	2	1	\N	199
12281	Kimwanga Medical Centre	KIMWANGAME-BUN-CA556B	019511		P.O BOX 2262-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:19.071+03	2025-09-01 19:58:19.071+03	2	1	\N	199
12282	Samaritan Eye  Retina Centre	SAMARITANE-BUN-0483A9	019550		P.O BOX 63- BUNGOMA MEDICAL CENTRE Private LEVEL 3A 15BUNGOMA LICENCED	t			2025-09-01 19:58:20.376+03	2025-09-01 19:58:20.376+03	2	1	\N	199
12283	Transelgon Healthcare Ltd - Cheptais	TRANSELGON-BUN-BB62B3	019551		P.O BOX 19- BUNGOMA MEDICAL CENTRE Private LEVEL 3A 15BUNGOMA LICENCED	t			2025-09-01 19:58:22.192+03	2025-09-01 19:58:22.192+03	2	1	\N	199
12284	Morimed Medical Clinic	MORIMEDMED-BUN-C5ACC0	019638		P.O BOX 1474-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:23.887+03	2025-09-01 19:58:23.887+03	2	1	\N	199
12285	Melita Medical Center	MELITAMEDI-BUN-A2FEFD	019816		P.O BOX 2552-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:25.678+03	2025-09-01 19:58:25.678+03	2	1	\N	199
12286	Bungoma Dental  Eye Care Centre Limited	BUNGOMADEN-BUN-F5E312	019876		P.O BOX 67-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED	t			2025-09-01 19:58:27.292+03	2025-09-01 19:58:27.292+03	2	1	\N	199
12287	Elephant Dental Limited-Bungoma	ELEPHANTDE-BUN-B0477B	019933		P.O BOX --- BUNGOMA DENTAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:29.108+03	2025-09-01 19:58:29.108+03	2	1	\N	199
12288	Equity Afia Limited- Bungoma Medical Centre	EQUITYAFIA-NAI-CC08BF	019952		P.O BOX 42752-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED	t			2025-09-01 19:58:30.618+03	2025-09-01 19:58:30.618+03	2	1	\N	194
12289	Eliane Royal Hospital Limited	ELIANEROYA-BUN-6CB37A	020200		P.O BOX 2211-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 30BUNGOMA LICENCED	t			2025-09-01 19:58:32.348+03	2025-09-01 19:58:32.348+03	2	1	\N	199
12290	Racia Hospital	RACIAHOSPI-BUN-C9314F	020767		P.O BOX 2495-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:33.671+03	2025-09-01 19:58:33.671+03	2	1	\N	199
12291	Chad Medical Centre	CHADMEDICA-BUN-9E824B	020975		P.O BOX 924-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:34.783+03	2025-09-01 19:58:34.783+03	2	1	\N	199
12292	Myanga Medical Clinic	MYANGAMEDI-BUN-F5B46F	021069		P.O BOX 571-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:36.204+03	2025-09-01 19:58:36.204+03	2	1	\N	199
12293	Olympia Medical Centre	OLYMPIAMED-BUN-A7C315	021100		P.O BOX 1699-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:37.698+03	2025-09-01 19:58:37.698+03	2	1	\N	199
12294	Nzoia Sugar Company	NZOIASUGAR-BUN-981788	006381		P.O BOX 285-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED	t			2025-09-01 19:58:38.833+03	2025-09-01 19:58:38.833+03	2	1	\N	199
12295	Edesa Medicare Bungoma	EDESAMEDIC-BUN-656E3F	018556		P.O BOX 519-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 8BUNGOMA LICENCED	t			2025-09-01 19:58:40.307+03	2025-09-01 19:58:40.307+03	2	1	\N	199
12296	Your Family Cfw Community Clinic	YOURFAMILY-NAI-8CEB60	001411		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:41.777+03	2025-09-01 19:58:41.777+03	2	1	\N	194
12297	Busia County Referral Hospital	BUSIACOUNT-BUS-6B1A74	GK-012543		P.O BOX 87-50400 BUSIA HOSPITAL LEVEL 4 Public LEVEL 4 149 BUSIA LICENCED	t			2025-09-01 19:58:43.611+03	2025-09-01 19:58:43.611+03	2	1	\N	202
12298	Kari Trc Alupe Hospital	KARITRCALU-BUS-13CBBA	GK-012749		P.O BOX 399-50400 BUSIA HEALTH CENTRE Public LEVEL 3B 12BUSIA LICENCED	t			2025-09-01 19:58:45.063+03	2025-09-01 19:58:45.063+03	2	1	\N	202
12299	Holy Family Hospital Nangina	HOLYFAMILY-BUS-6EE1C2	001195		P.O BOX 57-50406 FUNYULA FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 100 BUSIA LICENCED	t			2025-09-01 19:58:46.375+03	2025-09-01 19:58:46.375+03	2	1	\N	202
12300	Cornerstone Baptist	CORNERSTON-NAI-D3D954	013968		P.O BOX 2171-00200 NAIROBI FAITH BASED DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:46.462+03	2025-09-01 19:58:46.462+03	2	1	\N	194
12301	Tanaka Nursing Home Busia	TANAKANURS-BUS-B9250F	000225		P.O BOX 485-50400 BUSIA HOSPITAL LEVEL 4 Private LEVEL 4 110 BUSIA LICENCED	t			2025-09-01 19:58:47.835+03	2025-09-01 19:58:47.835+03	2	1	\N	202
12302	New Busia Maternity  Nursing Home	NEWBUSIAMA-BUS-3C6597	000318		P.O BOX 418-50400 BUSIA HOSPITAL LEVEL 4 Private LEVEL 4 60BUSIA LICENCED	t			2025-09-01 19:58:49.232+03	2025-09-01 19:58:49.232+03	2	1	\N	202
12303	Fahelma Cfw Community Clinic	FAHELMACFW-NAI-CD379C	001419		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:49.32+03	2025-09-01 19:58:49.32+03	2	1	\N	194
12304	Bumala Cfw Clinic	BUMALACFWC-NAI-23D44A	001961		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:50.756+03	2025-09-01 19:58:50.756+03	2	1	\N	194
12305	Namenya Cfw Clinic	NAMENYACFW-NAI-409F63	001969		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:50.839+03	2025-09-01 19:58:50.839+03	2	1	\N	194
12306	Pesi Medical Centre	PESIMEDICA-BUS-AE7B3D	002415		P.O BOX 94-50400 BUSIA NURSING HOME Private LEVEL 3B 18BUSIA LICENCED	t			2025-09-01 19:58:50.906+03	2025-09-01 19:58:50.906+03	2	1	\N	202
12307	The Aga Khan Hospital - Busia	THEAGAKHAN-BUS-B8752E	002815		P.O BOX 530-40100 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED	t			2025-09-01 19:58:50.972+03	2025-09-01 19:58:50.972+03	2	1	\N	202
12308	Feith Medical Clinic Busia	FEITHMEDIC-BUS-A4800F	003866		P.O BOX 574- BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:52.302+03	2025-09-01 19:58:52.302+03	2	1	\N	202
12309	Busia Equator Clinic	BUSIAEQUAT-BUS-6AAAC2	003916		P.O BOX 87-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:53.796+03	2025-09-01 19:58:53.796+03	2	1	\N	202
12310	Busia Base Boarder Faith Medical Centre	BUSIABASEB-BUS-2E5AA4	005833		P.O BOX 574-50400 BUSIA NURSING HOME Private LEVEL 3B 16BUSIA LICENCED	t			2025-09-01 19:58:55.614+03	2025-09-01 19:58:55.614+03	2	1	\N	202
12311	Stirling Healthcare Consultants	STIRLINGHE-BUS-96D3E2	007005		P.O BOX 313-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:57.765+03	2025-09-01 19:58:57.765+03	2	1	\N	202
12312	Busia Healthsidelab Medical Clinic	BUSIAHEALT-BUS-5CDA87	007211		P.O BOX 155-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:58:59.639+03	2025-09-01 19:58:59.639+03	2	1	\N	202
12313	Bunyala Medical Clinic	BUNYALAMED-KAK-46DB50	007367		P.O BOX 940-50100 KAKAMEGA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:01.572+03	2025-09-01 19:59:01.572+03	2	1	\N	200
12314	Optex Opticians Ltd - Busia	OPTEXOPTIC-BUS-AEEF50	007535		P.O BOX 11-50400 BUSIA EYE CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:03.393+03	2025-09-01 19:59:03.393+03	2	1	\N	202
12315	Visiongate Eye Care Consultant	VISIONGATE-BUS-782FF4	014441		P.O BOX 313-50400 BUSIA EYE CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:04.81+03	2025-09-01 19:59:04.81+03	2	1	\N	202
12316	Zurri Cottage Healthcare	ZURRICOTTA-BUS-85A145	014689		P.O BOX 514-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:06.378+03	2025-09-01 19:59:06.378+03	2	1	\N	202
12317	Minallahi Medicare	MINALLAHIM-BUS-CC0CF2	014999		P.O BOX -50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:07.798+03	2025-09-01 19:59:07.798+03	2	1	\N	202
12318	Bliss Healthcare Ltd Busia	BLISSHEALT-NAI-4B4A1C	015097		P.O BOX 5763-00200 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED	t			2025-09-01 19:59:09.612+03	2025-09-01 19:59:09.612+03	2	1	\N	194
12319	Amane Cottage Hospital	AMANECOTTA-ELD-FC4FBD	015151		P.O BOX 5532-30100 ELDORET COTTAGE HOSPITAL Private LEVEL 3B 13BUSIA LICENCED	t			2025-09-01 19:59:11.009+03	2025-09-01 19:59:11.009+03	2	1	\N	193
12320	Lumola Medical Clinic	LUMOLAMEDI-BUS-D42829	015554		P.O BOX 35-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED	t			2025-09-01 19:59:12.325+03	2025-09-01 19:59:12.325+03	2	1	\N	202
12321	Nassi Hospitals	NASSIHOSPI-BUS-7F1FCA	015596		P.O BOX 486-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 30BUSIA LICENCED	t			2025-09-01 19:59:13.624+03	2025-09-01 19:59:13.624+03	2	1	\N	202
12322	Medspar Medical Centre	MEDSPARMED-BUS-CA93E5	015832		P.O BOX 43-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:15.206+03	2025-09-01 19:59:15.206+03	2	1	\N	202
12323	Turning Point Medical Centre	TURNINGPOI-BUS-275E57	015994		P.O BOX 3-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED	t			2025-09-01 19:59:16.445+03	2025-09-01 19:59:16.445+03	2	1	\N	202
12324	Busia Medical Specialists And Diagnostic Centre	BUSIAMEDIC-BUS-58307D	016193		P.O BOX 2310-50200 BUSIA MEDICAL CENTRE Private LEVEL 3A 8BUSIA LICENCED	t			2025-09-01 19:59:17.953+03	2025-09-01 19:59:17.953+03	2	1	\N	202
12325	Brilliance Care Medical Hospital	BRILLIANCE-SIA-90EFCA	016568		P.O BOX 856-40600 SIAYA MEDICAL CENTRE Private LEVEL 3A 15BUSIA LICENCED	t			2025-09-01 19:59:19.619+03	2025-09-01 19:59:19.619+03	2	1	\N	203
12326	Ganga Cfw Clinic	GANGACFWCL-NAI-5F9A92	017017		P.O BOX 1630-00600 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:21.178+03	2025-09-01 19:59:21.178+03	2	1	\N	194
12327	Leben Medical Service-Busibwabo	LEBENMEDIC-KAK-386A3A	017732		P.O BOX 898-50100 KAKAMEGA NURSING HOME Private LEVEL 3B 40BUSIA LICENCED	t			2025-09-01 19:59:22.433+03	2025-09-01 19:59:22.433+03	2	1	\N	200
12328	Tomaps Medical Clinic	TOMAPSMEDI-KAK-F4754B	017783		P.O BOX 190-50100 KAKAMEGA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:23.93+03	2025-09-01 19:59:23.93+03	2	1	\N	200
12329	Brimaxa Hospital Limited	BRIMAXAHOS-NAI-24AD37	017872		P.O BOX 38133-00100 NAIROBI HOSPITAL LEVEL 4 Private LEVEL 4 60BUSIA LICENCED	t			2025-09-01 19:59:25.215+03	2025-09-01 19:59:25.215+03	2	1	\N	194
12330	Good Hope Health Limited	GOODHOPEHE-BUS-01AAA7	017921		P.O BOX 10548-30100 BUSIA HOSPITAL LEVEL 4 Private LEVEL 4 42BUSIA LICENCED	t			2025-09-01 19:59:26.508+03	2025-09-01 19:59:26.508+03	2	1	\N	202
12331	Raimu Hospital Limited-Malaba	RAIMUHOSPI-BUN-8C6C59	018466		P.O BOX 2448-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 25BUSIA LICENCED	t			2025-09-01 19:59:28.286+03	2025-09-01 19:59:28.286+03	2	1	\N	199
12332	St.James Infirmary Busia Limited	STJAMESINF-BUS-C8743F	018521		P.O BOX 1108-50400 BUSIA NURSING HOME Private LEVEL 3B 30BUSIA LICENCED	t			2025-09-01 19:59:29.591+03	2025-09-01 19:59:29.591+03	2	1	\N	202
12333	Oasis Doctors Plaza Busia Limited	OASISDOCTO-BUS-9A77F6	018613		P.O BOX 201-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED	t			2025-09-01 19:59:31.26+03	2025-09-01 19:59:31.26+03	2	1	\N	202
12334	Blossom Dental Clinic Ltd	BLOSSOMDEN-KIS-008978	019326		P.O BOX 2415-40100 KISUMU DENTAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:32.962+03	2025-09-01 19:59:32.962+03	2	1	\N	198
12335	Esikoma Community Hospital	ESIKOMACOM-KAK-2EFA18	020069		P.O BOX 2395-50100 KAKAMEGA MEDICAL CENTRE Private LEVEL 3A 18BUSIA LICENCED	t			2025-09-01 19:59:34.343+03	2025-09-01 19:59:34.343+03	2	1	\N	200
12336	Alinacare Health Services	ALINACAREH-BUS-6F92EF	020131		P.O BOX 302-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:35.691+03	2025-09-01 19:59:35.691+03	2	1	\N	202
12337	Chalondra Healthcare Clinic	CHALONDRAH-KIS-5FF81C	020236		P.O BOX 3232-40100 KISUMU MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED	t			2025-09-01 19:59:37.005+03	2025-09-01 19:59:37.005+03	2	1	\N	198
12338	Bulwani Priv Ate Hospital Limited	BULWANIPRI-BUS-D49BBC	020386		P.O BOX 64-50405 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED	t			2025-09-01 19:59:38.598+03	2025-09-01 19:59:38.598+03	2	1	\N	202
12339	Endo Health Centre Mission	ENDOHEALTH-ELD-9C0115	000416		P.O BOX 8409-30100 ELDORET HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 24ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:40.086+03	2025-09-01 19:59:40.086+03	2	1	\N	193
12340	Embobut Catholic Mission Dispensary	EMBOBUTCAT-ELD-8F7137	000469		P.O BOX 256-30705 ELDORET DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:41.371+03	2025-09-01 19:59:41.371+03	2	1	\N	193
12341	Kapkoi Health Centre	KAPKOIHEAL-ELD-C0016B	000415		P.O BOX 1890-30100 ELDORET HEALTH CENTRE Private LEVEL 3B 10ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:42.846+03	2025-09-01 19:59:42.846+03	2	1	\N	193
12342	Chesongoch Mission Hospital	CHESONGOCH-ELD-15D3E7	001960		P.O BOX 8409-30100 ELDORET FAITH BASED LEVEL 4 HOSPITAL Private LEVEL 4 56ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:42.95+03	2025-09-01 19:59:42.95+03	2	1	\N	193
12343	Bliss Healthcare Ltd Iten	BLISSHEALT-NAI-6E9CDD	007265		P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:44.447+03	2025-09-01 19:59:44.447+03	2	1	\N	194
12344	Cheptongei Medical Clinic	CHEPTONGEI-ELD-44F43C	014495		P.O BOX 3790-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:45.82+03	2025-09-01 19:59:45.82+03	2	1	\N	193
12345	Lj Malel Medical Centre Ltd	LJMALELMED-ELD-CF354F	016325		P.O BOX 10583-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:47.147+03	2025-09-01 19:59:47.147+03	2	1	\N	193
12346	Flax Sa V Anis Medical Centre	FLAXSAVANI-ELD-60C754	018563		P.O BOX 2594-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:48.275+03	2025-09-01 19:59:48.275+03	2	1	\N	193
12347	Invela Health Care Ltd	INVELAHEAL-ELD-C24D92	019007		P.O BOX 692-30100 ELDORET MEDICAL CENTRE Private LEVEL 3A 8ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:49.748+03	2025-09-01 19:59:49.748+03	2	1	\N	193
12348	Equity Afia Limited-Iten Medical Centre	EQUITYAFIA-NAI-5970E7	020825		P.O BOX 75104-00200 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0ELGEYO MARAKWET LICENCED	t			2025-09-01 19:59:51.368+03	2025-09-01 19:59:51.368+03	2	1	\N	194
12349	St. Augustine Cfw Clinic	STAUGUSTIN-NAI-0F220A	001957		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 19:59:52.802+03	2025-09-01 19:59:52.802+03	2	1	\N	194
12350	St. Anthony Cfw Clinic	STANTHONYC-NAI-C02A16	001978		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 19:59:54.214+03	2025-09-01 19:59:54.214+03	2	1	\N	194
12351	St. Nicholas C.F.W Clinic	STNICHOLAS-NAI-F931CE	001983		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 19:59:55.747+03	2025-09-01 19:59:55.747+03	2	1	\N	194
12352	Tender Loving Care Cfw Clinic	TENDERLOVI-NAI-153B46	001984		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 19:59:56.977+03	2025-09-01 19:59:56.977+03	2	1	\N	194
12353	Embu County Referral Hospital	EMBUCOUNTY-EMB-71E377	GK-008092		P.O BOX 33-60100 EMBU Hospital Level 5 Public LEVEL 5 618 EMBU LICENCED	t			2025-09-01 19:59:57.081+03	2025-09-01 19:59:57.081+03	2	1	\N	204
12354	University Of Embu Department Of Health Services	UNIVERSITY-EMB-FADF71	GK-011454		P.O BOX 6-60100 EMBU DISPENSARY Public LEVEL 2 0EMBU LICENCED	t			2025-09-01 19:59:58.43+03	2025-09-01 19:59:58.43+03	2	1	\N	204
12355	Consolata Hospital Kyeni	CONSOLATAH-EMB-F7D7F1	000791		P.O BOX 38-60103 RUNYENJES FAITH BASED LEVEL 5 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 5 280 EMBU LICENCED	t			2025-09-01 20:00:00.194+03	2025-09-01 20:00:00.194+03	2	1	\N	204
12356	Geltrude Health Centre	GELTRUDEHE-EMB-8B8497	000850		P.O BOX 2099-60100 EMBU HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 6EMBU LICENCED	t			2025-09-01 20:00:00.281+03	2025-09-01 20:00:00.281+03	2	1	\N	204
12357	Liviero Dispensary	LIVIERODIS-EMB-8BF8E2	000851		P.O BOX 2099-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:01.959+03	2025-09-01 20:00:01.959+03	2	1	\N	204
12358	St. Marys Dispensary Nguviu	STMARYSDIS-EMB-597446	001077		P.O BOX 194-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:02.141+03	2025-09-01 20:00:02.141+03	2	1	\N	204
12359	Ack Kiriari Dispensary	ACKKIRIARI-EMB-604A19	002307		P.O BOX 2467-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:02.238+03	2025-09-01 20:00:02.238+03	2	1	\N	204
12360	Mother Mazzarello Dispensary	MOTHERMAZZ-EMB-5DEBBC	005551		P.O BOX 1154-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:03.453+03	2025-09-01 20:00:03.453+03	2	1	\N	204
12361	Kevote Catholic Dispensary	KEVOTECATH-EMB-19C5F4	016484		P.O BOX 24-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:04.758+03	2025-09-01 20:00:04.758+03	2	1	\N	204
12362	Joykim Nursing Home	JOYKIMNURS-EMB-0370E5	000005		P.O BOX 986-60100 EMBU NURSING HOME Private LEVEL 3B 30EMBU LICENCED	t			2025-09-01 20:00:04.838+03	2025-09-01 20:00:04.838+03	2	1	\N	204
12363	Liberty Maternity And Nursing Home	LIBERTYMAT-EMB-D24FC6	000999		P.O BOX 2143-60100 EMBU NURSING HOME Private LEVEL 3B 26EMBU LICENCED	t			2025-09-01 20:00:04.919+03	2025-09-01 20:00:04.92+03	2	1	\N	204
12364	St. Teresa Cfw Clinic	STTERESACF-NAI-5FC08D	001966		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:05+03	2025-09-01 20:00:05+03	2	1	\N	194
12365	Faith Cfw Clinic	FAITHCFWCL-NAI-C93810	001968		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:06.226+03	2025-09-01 20:00:06.226+03	2	1	\N	194
12366	Afya Line Cfw Clinic	AFYALINECF-NAI-16F96E	001970		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:07.889+03	2025-09-01 20:00:07.889+03	2	1	\N	194
12367	Joy Cfw Clinic	JOYCFWCLIN-NAI-047B29	002019		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:09.163+03	2025-09-01 20:00:09.163+03	2	1	\N	194
12368	Patience Cfw Clinic	PATIENCECF-NAI-A63434	002023		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:10.474+03	2025-09-01 20:00:10.474+03	2	1	\N	194
12369	Mwea Dental Clinic	MWEADENTAL-EMB-F9A05A	002270		P.O BOX 1698- EMBU DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:11.891+03	2025-09-01 20:00:11.891+03	2	1	\N	204
12370	County Medical Centre Embu Ltd	COUNTYMEDI-EMB-DF2AF8	002537		P.O BOX 558-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 52EMBU LICENCED	t			2025-09-01 20:00:11.981+03	2025-09-01 20:00:11.981+03	2	1	\N	204
12371	Embu Childrens Clinic	EMBUCHILDR-EMB-4E19CB	002538		P.O BOX 1698-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 35EMBU LICENCED	t			2025-09-01 20:00:12.065+03	2025-09-01 20:00:12.065+03	2	1	\N	204
12372	Jetma Clinic	JETMACLINI-EMB-8A67FD	002746		P.O BOX 1569- EMBU MEDICAL CLINIC Private LEVEL 2 2EMBU LICENCED	t			2025-09-01 20:00:13.504+03	2025-09-01 20:00:13.504+03	2	1	\N	204
12373	Promise Cfw Clinic	PROMISECFW-NAI-F0F44D	002972		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:13.611+03	2025-09-01 20:00:13.611+03	2	1	\N	194
12374	Cfw Mbuvore Clinic	CFWMBUVORE-NAI-FEF11F	003060		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:14.822+03	2025-09-01 20:00:14.822+03	2	1	\N	194
12375	Kimangaru Cfw Clinic	KIMANGARUC-NAI-681733	003162		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:16.029+03	2025-09-01 20:00:16.029+03	2	1	\N	194
12376	The Aga Khan University Hospital Embu Clinic	THEAGAKHAN-NAI-B2C63D	003234		P.O BOX 30270-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED	t			2025-09-01 20:00:17.288+03	2025-09-01 20:00:17.288+03	2	1	\N	194
12377	Ka Vutiri Cfw Clinic	KAVUTIRICF-NAI-C6AC1B	003577		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:17.389+03	2025-09-01 20:00:17.389+03	2	1	\N	194
12378	Huruma Cfw Clinic	HURUMACFWC-NAI-CF050E	003612		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:18.781+03	2025-09-01 20:00:18.781+03	2	1	\N	194
12379	Focus Clinical And Diagnostic Centre Ltd Embu	FOCUSCLINI-EMB-EEE378	004095		P.O BOX 783-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED	t			2025-09-01 20:00:19.939+03	2025-09-01 20:00:19.939+03	2	1	\N	204
12380	Utugi Cfw Clinic	UTUGICFWCL-NAI-01902E	004172		P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:21.53+03	2025-09-01 20:00:21.53+03	2	1	\N	194
12381	Kings Care Medical Limited	KINGSCAREM-EMB-D4B3D3	004405		P.O BOX 1002-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 19EMBU LICENCED	t			2025-09-01 20:00:22.983+03	2025-09-01 20:00:22.983+03	2	1	\N	204
12382	Yunasi Medical Centre	YUNASIMEDI-MER-422CD1	005731		P.O BOX 2930-60200 MERU MEDICAL CENTRE Private LEVEL 3A 20EMBU LICENCED	t			2025-09-01 20:00:24.383+03	2025-09-01 20:00:24.383+03	2	1	\N	205
12383	Outspan Hospital Embu Medical Clinic	OUTSPANHOS-EMB-2F4800	005809		P.O BOX 2490-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:25.68+03	2025-09-01 20:00:25.68+03	2	1	\N	204
12384	Eastend Dental Clinic Limited	EASTENDDEN-NAI-42C13A	005822		P.O BOX 48580-00100 NAIROBI DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:27.07+03	2025-09-01 20:00:27.07+03	2	1	\N	194
12385	Potters Family Hospital	POTTERSFAM-EMB-BF3F16	007263		P.O BOX 1822-60100 EMBU NURSING HOME Private LEVEL 3B 50EMBU LICENCED	t			2025-09-01 20:00:27.264+03	2025-09-01 20:00:27.264+03	2	1	\N	204
12386	Greenspan Medical Centre	GREENSPANM-EMB-B08528	007572		P.O BOX 534-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 15EMBU LICENCED	t			2025-09-01 20:00:28.522+03	2025-09-01 20:00:28.522+03	2	1	\N	204
12387	Optident Dental Care	OPTIDENTDE-NAI-CEB472	008042		P.O BOX 103597-00101 NAIROBI DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:29.784+03	2025-09-01 20:00:29.784+03	2	1	\N	194
12388	Makutano Family Healthcare Services	MAKUTANOFA-EMB-79DC2D	008056		P.O BOX 2477-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:30.951+03	2025-09-01 20:00:30.951+03	2	1	\N	204
12389	Kirimara Opticals Ltd Embu	KIRIMARAOP-EMB-E639F3	012273		P.O BOX 2108-60100 EMBU EYE CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:32.434+03	2025-09-01 20:00:32.434+03	2	1	\N	204
12390	Daima Medical Clinic-Dallas	DAIMAMEDIC-EMB-09D863	014713		P.O BOX 1905-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:33.8+03	2025-09-01 20:00:33.8+03	2	1	\N	204
12392	Angel Care Medical Clinic	ANGELCAREM-EMB-840E32	014773		P.O BOX 50- EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:36.976+03	2025-09-01 20:00:36.976+03	2	1	\N	204
12393	Embu Tumaini Medical Services	EMBUTUMAIN-EMB-842D50	014977		P.O BOX 2211-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:38.182+03	2025-09-01 20:00:38.182+03	2	1	\N	204
12394	Elimundani Health Care Kiritiri	ELIMUNDANI-NAI-801F36	014984		P.O BOX 25493-00603 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:39.534+03	2025-09-01 20:00:39.534+03	2	1	\N	194
12395	Embu Children Hospital Tenri Makima	EMBUCHILDR-EMB-29F1C2	015053		P.O BOX 1698-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:41.082+03	2025-09-01 20:00:41.082+03	2	1	\N	204
12396	Smart Smile Dental Center	SMARTSMILE-EMB-7A7304	015074		P.O BOX 329-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED	t			2025-09-01 20:00:42.583+03	2025-09-01 20:00:42.584+03	2	1	\N	204
12397	Embu Medical And Dental Clinic	EMBUMEDICA-EMB-E228CB	015086		P.O BOX 1191-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:43.919+03	2025-09-01 20:00:43.919+03	2	1	\N	204
12398	Imara Hospital	IMARAHOSPI-EMB-786248	015246		P.O BOX 1446-60100 EMBU NURSING HOME Private LEVEL 3B 12EMBU LICENCED	t			2025-09-01 20:00:45.202+03	2025-09-01 20:00:45.202+03	2	1	\N	204
12399	Shanwes Med Care	SHANWESMED-MER-D0B998	015306		P.O BOX 2558-60200 MERU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:45.314+03	2025-09-01 20:00:45.314+03	2	1	\N	205
12400	Mt Kenya Heart And Diabetes Centre	MTKENYAHEA-NAI-4C972D	015409		P.O BOX 940-00618 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:46.598+03	2025-09-01 20:00:46.598+03	2	1	\N	194
12401	Visionners Medical Centre	VISIONNERS-EMB-C51EF9	015444		P.O BOX 194-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 30EMBU LICENCED	t			2025-09-01 20:00:48.528+03	2025-09-01 20:00:48.528+03	2	1	\N	204
12402	Murithi Metho Optometrist	MURITHIMET-EMB-731025	015632		P.O BOX 2475-60100 EMBU EYE CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:50.433+03	2025-09-01 20:00:50.433+03	2	1	\N	204
12403	Pure Medcare Clinic	PUREMEDCAR-EMB-6CBA87	015796		P.O BOX 712-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:52.087+03	2025-09-01 20:00:52.087+03	2	1	\N	204
12404	Kianjokoma Muungano Community Cottage Hospital	KIANJOKOMA-EMB-AADB3F	016023		P.O BOX 2162-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 15EMBU LICENCED	t			2025-09-01 20:00:53.536+03	2025-09-01 20:00:53.536+03	2	1	\N	204
12405	Frev Ane Hospital	FREVANEHOS-EMB-D99A42	016079		P.O BOX 755-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 50EMBU LICENCED	t			2025-09-01 20:00:55.431+03	2025-09-01 20:00:55.431+03	2	1	\N	204
12406	Mercy Medical Clinic-Embu	MERCYMEDIC-EMB-B6E309	016136		P.O BOX 1065-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:00:56.774+03	2025-09-01 20:00:56.774+03	2	1	\N	204
12407	St. Jude Medical Care	STJUDEMEDI-EMB-1CA4C0	016200		P.O BOX 205-60100 EMBU NURSING HOME Private LEVEL 3B 15EMBU LICENCED	t			2025-09-01 20:00:56.883+03	2025-09-01 20:00:56.883+03	2	1	\N	204
12408	Generation And Visionary Medical Centre	GENERATION-NAI-954C11	016692		P.O BOX 28760-00200 NAIROBI NURSING HOME Private LEVEL 3B 35EMBU LICENCED	t			2025-09-01 20:00:57.018+03	2025-09-01 20:00:57.018+03	2	1	\N	194
12409	Mount Hermon Medical Centre	MOUNTHERMO-EMB-9E8EDF	017066		P.O BOX 2676-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED	t			2025-09-01 20:00:59.126+03	2025-09-01 20:00:59.126+03	2	1	\N	204
12410	Mariari Ebenzer Medical Clinic	MARIARIEBE-NAI-FF977A	017191		P.O BOX 85845-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:00.907+03	2025-09-01 20:01:00.907+03	2	1	\N	194
12411	Amaze Dental Limited	AMAZEDENTA-EMB-23D649	017260		P.O BOX 1529-60100 EMBU DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:02.494+03	2025-09-01 20:01:02.494+03	2	1	\N	204
12412	Highrise Health Care Services	HIGHRISEHE-EMB-E5FE2A	017325		P.O BOX 254716153318-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:04.039+03	2025-09-01 20:01:04.039+03	2	1	\N	204
12413	Greensprings Medical Medical Clinic	GREENSPRIN-EMB-8518E5	017382		P.O BOX 1002-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:05.568+03	2025-09-01 20:01:05.568+03	2	1	\N	204
12414	Royal Smiles Dental Clinic Embu	ROYALSMILE-EMB-6C7415	017565		P.O BOX 510-60100 EMBU DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:07.357+03	2025-09-01 20:01:07.357+03	2	1	\N	204
12415	Granton  Dolly Nursing Home Limited	GRANTONDOL-EMB-5858D2	017607		P.O BOX 109-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 40EMBU LICENCED	t			2025-09-01 20:01:08.785+03	2025-09-01 20:01:08.785+03	2	1	\N	204
12416	Kiambere Medical Healthcare Limited	KIAMBEREME-EMB-4E7F23	017863		P.O BOX 140-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 34EMBU LICENCED	t			2025-09-01 20:01:10.221+03	2025-09-01 20:01:10.221+03	2	1	\N	204
12417	Nairobi Radiotherapy  Cancer Centre Limited-Embu	NAIROBIRAD-NAI-0BF4D0	017962		P.O BOX 3280-00506 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED	t			2025-09-01 20:01:12.271+03	2025-09-01 20:01:12.271+03	2	1	\N	194
12418	Patocare Medical Centre	PATOCAREME-EMB-94ACCC	018262		P.O BOX 84-10303 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:13.934+03	2025-09-01 20:01:13.934+03	2	1	\N	204
12419	V Alley View Medical Specialist And Diagnostic Embu Limited	VALLEYVIEW-EMB-25910E	018516		P.O BOX 2777-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED	t			2025-09-01 20:01:15.278+03	2025-09-01 20:01:15.278+03	2	1	\N	204
12420	Tumaini Medical Centre Rwika	TUMAINIMED-EMB-C12380	018545		P.O BOX 369-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:17.257+03	2025-09-01 20:01:17.257+03	2	1	\N	204
12421	Mbuvori Prime Medical Clinic	MBUVORIPRI-EMB-56F87E	019144		P.O BOX 591-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:18.77+03	2025-09-01 20:01:18.77+03	2	1	\N	204
12422	Marini-Medical Centre Ltd	MARINIMEDI-EMB-CDC539	019154		P.O BOX 35-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:20.552+03	2025-09-01 20:01:20.552+03	2	1	\N	204
12423	Cynerd Healthcare Group Limited	CYNERDHEAL-EMB-49442E	019167		P.O BOX 1217-60100 EMBU NURSING HOME Private LEVEL 3B 45EMBU LICENCED	t			2025-09-01 20:01:22.013+03	2025-09-01 20:01:22.013+03	2	1	\N	204
12424	Magnificent Medical Centre	MAGNIFICEN-EMB-A6E3C3	019221		P.O BOX 280-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:23.607+03	2025-09-01 20:01:23.607+03	2	1	\N	204
12425	Serenity Homes Rehabilitation And Counselling Center Limited	SERENITYHO-EMB-E63A42	019351		P.O BOX 660-60100 EMBU NURSING HOME Private LEVEL 3B 50EMBU LICENCED	t			2025-09-01 20:01:24.845+03	2025-09-01 20:01:24.845+03	2	1	\N	204
12426	Pleroma Medical Centre	PLEROMAMED-EMB-D37041	019455		P.O BOX 2546-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:26.689+03	2025-09-01 20:01:26.69+03	2	1	\N	204
12427	Vicoptic Eyeclinic Limited	VICOPTICEY-EMB-CA17FE	019467		P.O BOX 143-60100 EMBU EYE CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:28.107+03	2025-09-01 20:01:28.107+03	2	1	\N	204
12428	Imara Hospital Embu	IMARAHOSPI-EMB-F2B5E9	019531		P.O BOX 1446-60100 EMBU HOSPITAL LEVEL 4INTERNSHIP TRAINING CENTRECOUNTY HOSPITAL Private LEVEL 4 90EMBU LICENCED	t			2025-09-01 20:01:29.582+03	2025-09-01 20:01:29.582+03	2	1	\N	204
12429	Loyalty Hope Clinic	LOYALTYHOP-EMB-82A444	019671		P.O BOX 130-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:30.781+03	2025-09-01 20:01:30.781+03	2	1	\N	204
12430	Njukiri Medical Centre	NJUKIRIMED-EMB-E51870	019724		P.O BOX 850-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:31.983+03	2025-09-01 20:01:31.983+03	2	1	\N	204
12431	Embu Premier Physicians Limited	EMBUPREMIE-EMB-5A55D6	019860		P.O BOX 2586-00100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:33.124+03	2025-09-01 20:01:33.124+03	2	1	\N	204
12432	The Paradox Hospitals	THEPARADOX-EMB-5122C2	019880		P.O BOX 618-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:34.789+03	2025-09-01 20:01:34.789+03	2	1	\N	204
12433	Kiritiri Funeral Home	KIRITIRIFU-EMB-7935C7	019999		P.O BOX 2851-60100 EMBU FUNERAL HOME (STAND ALONE) Private LEVEL 3A 30EMBU LICENCED	t			2025-09-01 20:01:36.533+03	2025-09-01 20:01:36.533+03	2	1	\N	204
12434	Forealtors Hospital Ltd	FOREALTORS-EMB-7D4FEA	020023		P.O BOX 278-60103 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:38.009+03	2025-09-01 20:01:38.009+03	2	1	\N	204
12435	Walter Medical And Dental Care	WALTERMEDI-EMB-ADB788	020095		P.O BOX 1333-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:39.361+03	2025-09-01 20:01:39.361+03	2	1	\N	204
12436	Framary Medical Centre	FRAMARYMED-EMB-1E2F47	020235		P.O BOX 33-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:40.736+03	2025-09-01 20:01:40.736+03	2	1	\N	204
12437	Ericare Medical And Physiotherapy Services	ERICAREMED-EMB-D30F82	020278		P.O BOX 29-60125 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:42.014+03	2025-09-01 20:01:42.014+03	2	1	\N	204
12438	Emmanuel Meka Medical Clinic	EMMANUELME-EMB-B4EDE5	020496		P.O BOX 168-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:43.394+03	2025-09-01 20:01:43.394+03	2	1	\N	204
12439	Neema Universal Health Care Limited-Embu Town	NEEMAUNIVE-EMB-CFBB2F	020828		P.O BOX 2228-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 71EMBU LICENCED	t			2025-09-01 20:01:45.215+03	2025-09-01 20:01:45.215+03	2	1	\N	204
12440	Fountain Of Hope Medical Clinic	FOUNTAINOF-EMB-5EAE36	020931		P.O BOX 1905-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:46.894+03	2025-09-01 20:01:46.894+03	2	1	\N	204
12441	Kamiu Junction Community Health Centre	KAMIUJUNCT-EMB-1484DE	021129		P.O BOX 33-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:47.009+03	2025-09-01 20:01:47.009+03	2	1	\N	204
12442	Graceview Medical Center	GRACEVIEWM-EMB-3779AB	18011		P.O BOX 33-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:48.502+03	2025-09-01 20:01:48.502+03	2	1	\N	204
12443	Kengen Gitaru Staff Clinic	KENGENGITA-EMB-C8872F	002374		P.O BOX 205-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED	t			2025-09-01 20:01:49.815+03	2025-09-01 20:01:49.815+03	2	1	\N	204
12444	Garissa Mother And Child Health Care	GARISSAMOT-GAR-570ABA	002752		P.O BOX 547-- GARISSA NURSING HOME Private LEVEL 3B 14GARISSA LICENCED	t			2025-09-01 20:01:51.308+03	2025-09-01 20:01:51.308+03	2	1	\N	206
12445	Towba Medical Care	TOWBAMEDIC-GAR-E21772	001619		P.O BOX 445-70100 GARISSA HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 0GARISSA LICENCED	t			2025-09-01 20:01:52.884+03	2025-09-01 20:01:52.884+03	2	1	\N	206
12446	Bulla Hagar Dispensary	BULLAHAGAR-GAR-D288F8	002095		P.O BOX 808-70100 GARISSA DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:01:54.101+03	2025-09-01 20:01:54.101+03	2	1	\N	206
12447	Iom Migration Assesment Centre Dadaab	IOMMIGRATI-NAI-90C4EF	001168		P.O BOX 55040-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:01:54.209+03	2025-09-01 20:01:54.209+03	2	1	\N	194
12448	Garissa Nursing Home	GARISSANUR-GAR-F0A221	000265		P.O BOX 269-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 50GARISSA LICENCED	t			2025-09-01 20:01:56.118+03	2025-09-01 20:01:56.118+03	2	1	\N	206
12449	Simaho Mchfp Clinic	SIMAHOMCHF-GAR-0989AE	000646		P.O BOX 545-70100 GARISSA HEALTH CENTRE Private LEVEL 3B 14GARISSA LICENCED	t			2025-09-01 20:01:56.31+03	2025-09-01 20:01:56.31+03	2	1	\N	206
12450	Noorhilac Pharmaceutical Limited	NOORHILACP-GAR-22C22E	000896		P.O BOX 197-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 3GARISSA LICENCED	t			2025-09-01 20:01:57.771+03	2025-09-01 20:01:57.771+03	2	1	\N	206
12451	Excel Health Services Garissa	EXCELHEALT-GAR-2DCEF5	001506		P.O BOX 501-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED	t			2025-09-01 20:01:59.223+03	2025-09-01 20:01:59.223+03	2	1	\N	206
12452	Medina Medicare Hospital Limited	MEDINAMEDI-GAR-43C497	002130		P.O BOX 126-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 50GARISSA LICENCED	t			2025-09-01 20:02:00.88+03	2025-09-01 20:02:00.88+03	2	1	\N	206
12453	Tawheed Community Nursing Home	TAWHEEDCOM-GAR-3557D6	002517		P.O BOX 1419-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 52GARISSA LICENCED	t			2025-09-01 20:02:02.655+03	2025-09-01 20:02:02.655+03	2	1	\N	206
12454	North Eastern Medical Centre	NORTHEASTE-GAR-D83C7C	002546		P.O BOX 720-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:02:03.978+03	2025-09-01 20:02:03.978+03	2	1	\N	206
12455	Medina Hospital	MEDINAHOSP-GAR-BEDFAD	002813		P.O BOX 126-70100 GARISSA Hospital Level 5 Private LEVEL 5 110 GARISSA LICENCED	t			2025-09-01 20:02:05.151+03	2025-09-01 20:02:05.151+03	2	1	\N	206
12456	Womens Initiative Health Care Services	WOMENSINIT-GAR-919008	002987		P.O BOX 545-70100 GARISSA HEALTH CENTRE Private LEVEL 3B 10GARISSA LICENCED	t			2025-09-01 20:02:05.359+03	2025-09-01 20:02:05.359+03	2	1	\N	206
12457	Alliance Medical Centre Ltd Garissa	ALLIANCEME-GAR-C24525	003065		P.O BOX 1808-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 60GARISSA LICENCED	t			2025-09-01 20:02:07.045+03	2025-09-01 20:02:07.045+03	2	1	\N	206
12458	Cosgurow Healthcare Limited	COSGUROWHE-GAR-515A24	003075		P.O BOX 176-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 16GARISSA LICENCED	t			2025-09-01 20:02:08.622+03	2025-09-01 20:02:08.622+03	2	1	\N	206
12459	Al-Maqdis Medical Centre	ALMAQDISME-GAR-D7E6A1	003125		P.O BOX 470-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 42GARISSA LICENCED	t			2025-09-01 20:02:09.969+03	2025-09-01 20:02:09.969+03	2	1	\N	206
12460	Al Amin Medical  Labaratory	ALAMINMEDI-GAR-460AA0	003172		P.O BOX 29-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:11.07+03	2025-09-01 20:02:11.07+03	2	1	\N	206
12461	Garissa Childrens Hospital Ltd	GARISSACHI-GAR-2F9356	003440		P.O BOX 514-70100 GARISSA NURSING HOME Private LEVEL 3B 16GARISSA LICENCED	t			2025-09-01 20:02:12.502+03	2025-09-01 20:02:12.502+03	2	1	\N	206
12462	Count Medical And Diagnostic Limited	COUNTMEDIC-GAR-547099	003526		P.O BOX 1538-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 45GARISSA LICENCED	t			2025-09-01 20:02:14.369+03	2025-09-01 20:02:14.369+03	2	1	\N	206
12463	Zensturion Community Health Services	ZENSTURION-GAR-8BB6B3	003561		P.O BOX 151-60103 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:15.764+03	2025-09-01 20:02:15.764+03	2	1	\N	206
12464	Afnaan Healthcare Services	AFNAANHEAL-GAR-7D3C3A	003715		P.O BOX 486-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 11GARISSA LICENCED	t			2025-09-01 20:02:17.601+03	2025-09-01 20:02:17.601+03	2	1	\N	206
12465	Hilwa Medical Centre	HILWAMEDIC-GAR-FA9D04	004077		P.O BOX 523-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:18.972+03	2025-09-01 20:02:18.972+03	2	1	\N	206
12466	Al -Bushra Medical Centre	ALBUSHRAME-GAR-688F76	004151		P.O BOX 15 - GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:19.064+03	2025-09-01 20:02:19.064+03	2	1	\N	206
12467	Medina Medicare Hospital Limited-Hagardera	MEDINAMEDI-GAR-305CB9	005521		P.O BOX 126-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED	t			2025-09-01 20:02:19.163+03	2025-09-01 20:02:19.163+03	2	1	\N	206
12468	Familyfirst Medical Centre Limited	FAMILYFIRS-GAR-783166	005797		P.O BOX 1412-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED	t			2025-09-01 20:02:20.811+03	2025-09-01 20:02:20.811+03	2	1	\N	206
12469	Northgate Hospital Limited	NORTHGATEH-GAR-AF217D	005800		P.O BOX 1112-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 50GARISSA LICENCED	t			2025-09-01 20:02:22.026+03	2025-09-01 20:02:22.026+03	2	1	\N	206
12470	Jihan Medical Centre	JIHANMEDIC-GAR-2B34E1	005840		P.O BOX 1270-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:23.195+03	2025-09-01 20:02:23.195+03	2	1	\N	206
12471	Garissa Doctors Plaza	GARISSADOC-GAR-69CA1E	005863		P.O BOX 1558-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 52GARISSA LICENCED	t			2025-09-01 20:02:24.236+03	2025-09-01 20:02:24.236+03	2	1	\N	206
12472	Tasneem Medical Clinic	TASNEEMMED-GAR-F46FCA	006905		P.O BOX 983-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:25.843+03	2025-09-01 20:02:25.843+03	2	1	\N	206
12473	Al-Rashad Medical Centre	ALRASHADME-GAR-E5E107	007074		P.O BOX 60-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:27.164+03	2025-09-01 20:02:27.164+03	2	1	\N	206
12474	Sunna Healthcare  Dental Services	SUNNAHEALT-NAI-C75EB9	007095		P.O BOX 9279-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED	t			2025-09-01 20:02:28.408+03	2025-09-01 20:02:28.408+03	2	1	\N	194
12475	Ankara Medical Center Limited	ANKARAMEDI-GAR-EAB16B	007177		P.O BOX 973-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:02:29.715+03	2025-09-01 20:02:29.715+03	2	1	\N	206
12476	Garissa Ent Medical Centre	GARISSAENT-GAR-D9824F	007238		P.O BOX 1857-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 27GARISSA LICENCED	t			2025-09-01 20:02:31.347+03	2025-09-01 20:02:31.347+03	2	1	\N	206
12477	Anfac Nursing Home	ANFACNURSI-GAR-95F4EA	008603		P.O BOX 365-70100 GARISSA NURSING HOME Private LEVEL 3B 12GARISSA LICENCED	t			2025-09-01 20:02:32.614+03	2025-09-01 20:02:32.614+03	2	1	\N	206
12478	Masalani Diagnostic Limited	MASALANIDI-GAR-936F94	014720		P.O BOX 65-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED	t			2025-09-01 20:02:33.745+03	2025-09-01 20:02:33.745+03	2	1	\N	206
12479	Al-Qudus Medical Centre Ltd	ALQUDUSMED-GAR-34EFF4	014776		P.O BOX 953-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:02:35.115+03	2025-09-01 20:02:35.115+03	2	1	\N	206
12480	Madogashe Medical Services	MADOGASHEM-GAR-869F70	014864		P.O BOX 23-70102 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED	t			2025-09-01 20:02:35.213+03	2025-09-01 20:02:35.213+03	2	1	\N	206
12481	Modogashe Nursing Home	MODOGASHEN-GAR-3D2E83	014930		P.O BOX 73-70100 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED	t			2025-09-01 20:02:36.738+03	2025-09-01 20:02:36.738+03	2	1	\N	206
12482	Garissa Nursing Home Annex	GARISSANUR-GAR-D4E817	015027		P.O BOX 269-70100 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED	t			2025-09-01 20:02:36.862+03	2025-09-01 20:02:36.862+03	2	1	\N	206
12483	Antaliya Hospital Limited	ANTALIYAHO-GAR-1DA9F1	015462		P.O BOX 448-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 35GARISSA LICENCED	t			2025-09-01 20:02:38.103+03	2025-09-01 20:02:38.103+03	2	1	\N	206
12484	Dagahley Medical Health Care Services Limited	DAGAHLEYME-GAR-CA6D77	015536		P.O BOX 20-70100 GARISSA NURSING HOME Private LEVEL 3B 22GARISSA LICENCED	t			2025-09-01 20:02:39.306+03	2025-09-01 20:02:39.306+03	2	1	\N	206
12485	Highgate Healthcare Limited	HIGHGATEHE-GAR-A9DBBB	015783		P.O BOX 140-07100 GARISSA MEDICAL CENTRE Private LEVEL 3A 8GARISSA LICENCED	t			2025-09-01 20:02:40.694+03	2025-09-01 20:02:40.694+03	2	1	\N	206
12486	Sarap Medical Centre	SARAPMEDIC-GAR-4AAB04	016092		P.O BOX 341-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 10GARISSA LICENCED	t			2025-09-01 20:02:42.5+03	2025-09-01 20:02:42.5+03	2	1	\N	206
12487	Garissa Eye Hospital Ltd	GARISSAEYE-GAR-6351F7	016142		P.O BOX 1474-70100 GARISSA EYE HOSPITAL LEVEL 4 Private LEVEL 4 16GARISSA LICENCED	t			2025-09-01 20:02:43.561+03	2025-09-01 20:02:43.561+03	2	1	\N	206
12488	Jamia Islamic Intergrated Health Services	JAMIAISLAM-GAR-8BB60D	016364		P.O BOX 126-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED	t			2025-09-01 20:02:44.806+03	2025-09-01 20:02:44.806+03	2	1	\N	206
12489	Hamdan Medical Centre	HAMDANMEDI-GAR-607128	016482		P.O BOX 40701- GARISSA MEDICAL CENTRE Private LEVEL 3A 14GARISSA LICENCED	t			2025-09-01 20:02:46.32+03	2025-09-01 20:02:46.32+03	2	1	\N	206
12490	Gacal Budget Hospital	GACALBUDGE-GAR-41CDE8	016701		P.O BOX 553-70100 GARISSA NURSING HOME Private LEVEL 3B 50GARISSA LICENCED	t			2025-09-01 20:02:47.487+03	2025-09-01 20:02:47.487+03	2	1	\N	206
12491	Samara Medical Centre	SAMARAMEDI-GAR-58C6B3	017091		P.O BOX 830-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED	t			2025-09-01 20:02:48.762+03	2025-09-01 20:02:48.762+03	2	1	\N	206
12492	Al-Dayax Medical Clinic And Laboratory Services	ALDAYAXMED-GAR-837E02	017118		P.O BOX 126-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:50.27+03	2025-09-01 20:02:50.27+03	2	1	\N	206
12493	Mbassy Medical Centre Limited	MBASSYMEDI-GAR-71C68F	017123		P.O BOX 514-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 10GARISSA LICENCED	t			2025-09-01 20:02:51.766+03	2025-09-01 20:02:51.766+03	2	1	\N	206
12494	Star Dental Clinics Limited	STARDENTAL-NAI-3A4D6D	017180		P.O BOX 7883-00610 NAIROBI DENTAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:53.05+03	2025-09-01 20:02:53.05+03	2	1	\N	194
12495	Tawheed Medical Clinic	TAWHEEDMED-GAR-EFF3C5	017838		P.O BOX 1419-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:54.336+03	2025-09-01 20:02:54.336+03	2	1	\N	206
12496	Dobale Clinic	DOBALECLIN-GAR-B2AFF0	018761		P.O BOX 256-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:02:55.967+03	2025-09-01 20:02:55.967+03	2	1	\N	206
12497	Shifa Maternal And Child Care Limited	SHIFAMATER-GAR-ECA8CE	018917		P.O BOX 658-70100 GARISSA NURSING HOME Private LEVEL 3B 30GARISSA LICENCED	t			2025-09-01 20:02:57.525+03	2025-09-01 20:02:57.525+03	2	1	\N	206
12498	Nep Nursing And Rehabilitation Centre	NEPNURSING-GAR-33CA5D	019159		P.O BOX 23-70100 GARISSA REHABILITATION CENTRE Private LEVEL 3A 10GARISSA LICENCED	t			2025-09-01 20:02:59.441+03	2025-09-01 20:02:59.441+03	2	1	\N	206
12499	Sa V Annah Royal Hospital Garissa Limited	SAVANNAHRO-NAI-1CE525	019344		P.O BOX 20617-00100 NAIROBI HOSPITAL LEVEL 4 Private LEVEL 4 65GARISSA LICENCED	t			2025-09-01 20:03:01.238+03	2025-09-01 20:03:01.238+03	2	1	\N	194
12500	Emirates Hospital Limited	EMIRATESHO-GAR-0AA287	019391		P.O BOX 311-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED	t			2025-09-01 20:03:02.708+03	2025-09-01 20:03:02.708+03	2	1	\N	206
12501	Al-Baitul Tiiba Hospital Limited	ALBAITULTI-GAR-784A12	019465		P.O BOX 882-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED	t			2025-09-01 20:03:04.057+03	2025-09-01 20:03:04.057+03	2	1	\N	206
12502	Jidah Medical Centre Limited	JIDAHMEDIC-GAR-B6A7A2	019721		P.O BOX 610-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:03:05.772+03	2025-09-01 20:03:05.772+03	2	1	\N	206
12503	Top Care Orthopaedic And Trauma Centre Limited	TOPCAREORT-GAR-FBCCBE	019932		P.O BOX 256-70100 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED	t			2025-09-01 20:03:06.947+03	2025-09-01 20:03:06.947+03	2	1	\N	206
12504	An Najah Medical Care Limited	ANNAJAHMED-GAR-DA1E85	019965		P.O BOX 575-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 20GARISSA LICENCED	t			2025-09-01 20:03:08.476+03	2025-09-01 20:03:08.476+03	2	1	\N	206
12505	Al Qudus Diagnostic Hospital.	ALQUDUSDIA-GAR-9177EC	019979		P.O BOX 374-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED	t			2025-09-01 20:03:08.599+03	2025-09-01 20:03:08.599+03	2	1	\N	206
12506	Salama Wellness Centre Limited	SALAMAWELL-GAR-23E85E	020036		P.O BOX 782-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 25GARISSA LICENCED	t			2025-09-01 20:03:10.433+03	2025-09-01 20:03:10.433+03	2	1	\N	206
12507	Garissa University Clinic	GARISSAUNI-GAR-3796F0	020148		P.O BOX 1801-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:03:11.754+03	2025-09-01 20:03:11.754+03	2	1	\N	206
12508	Madyan Nursing Home Limited	MADYANNURS-GAR-9226C5	020419		P.O BOX 171-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED	t			2025-09-01 20:03:13.071+03	2025-09-01 20:03:13.071+03	2	1	\N	206
12509	Al-Maqdis Medical Centre Annex Limited	ALMAQDISME-GAR-C1593C	020439		P.O BOX 470-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:03:14.221+03	2025-09-01 20:03:14.221+03	2	1	\N	206
12510	Bayan Eye Care Limited	BAYANEYECA-GAR-D38CBC	020448		P.O BOX 1520-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:03:15.67+03	2025-09-01 20:03:15.67+03	2	1	\N	206
12511	Al Hadaf Medical Clinic	ALHADAFMED-GAR-E088C3	020614		P.O BOX 209-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:03:16.817+03	2025-09-01 20:03:16.817+03	2	1	\N	206
12512	Abuu Amira Nursing Home	ABUUAMIRAN-GAR-FEF661	020621		P.O BOX 405-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:03:18.156+03	2025-09-01 20:03:18.156+03	2	1	\N	206
12513	International Optica Clinic Garissa	INTERNATIO-GAR-C44F0D	020644		P.O BOX 86002-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:03:19.426+03	2025-09-01 20:03:19.426+03	2	1	\N	206
12514	Tolsan Medical Center	TOLSANMEDI-GAR-802D28	020858		P.O BOX 70100-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:03:21.08+03	2025-09-01 20:03:21.08+03	2	1	\N	206
12515	Malifisa Hospital Limited	MALIFISAHO-GAR-C1400B	020907		P.O BOX 103-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED	t			2025-09-01 20:03:22.44+03	2025-09-01 20:03:22.44+03	2	1	\N	206
12516	Garissa Eye And Orthodontics Hospital Limited	GARISSAEYE-GAR-31B871	020984		P.O BOX 1474-70100 GARISSA NURSING HOME Private LEVEL 3B 4GARISSA LICENCED	t			2025-09-01 20:03:23.572+03	2025-09-01 20:03:23.572+03	2	1	\N	206
12517	Anfal Medical Center Limited	ANFALMEDIC-GAR-981E8A	021006		P.O BOX 514-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED	t			2025-09-01 20:03:25.122+03	2025-09-01 20:03:25.122+03	2	1	\N	206
12518	Dr Smile Dental Clinic Limited	DRSMILEDEN-GAR-428477	021018		P.O BOX 254727670640-70100 GARISSA DENTAL CLINIC Private LEVEL 2 0GARISSA LICENCED	t			2025-09-01 20:03:26.262+03	2025-09-01 20:03:26.262+03	2	1	\N	206
12519	Arqam Medical Centre	ARQAMMEDIC-GAR-1F058D	021080		P.O BOX 39-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED	t			2025-09-01 20:03:27.708+03	2025-09-01 20:03:27.708+03	2	1	\N	206
12520	Waberi Hospital Ltd	WABERIHOSP-GAR-2237D1	014373		P.O BOX 957-70100 GARISSA NURSING HOME Private LEVEL 3B 40GARISSA LICENCED	t			2025-09-01 20:03:28.702+03	2025-09-01 20:03:28.702+03	2	1	\N	206
12521	Reusse Troyer Mission Health Centre	REUSSETROY-MIG-B29EDA	001254		P.O BOX 844-40400 MIGORI HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 6HOMA BAY LICENCED	t			2025-09-01 20:03:30.074+03	2025-09-01 20:03:30.074+03	2	1	\N	201
12522	F.S.J St. Theresa Asumbi Mission Hospital	FSJSTTHERE-KIS-B43725	001662		P.O BOX 669-40200 KISII FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 73HOMA BAY LICENCED	t			2025-09-01 20:03:31.694+03	2025-09-01 20:03:31.694+03	2	1	\N	207
12523	St Theresa Fsj Asumbi Rodi Dispensary	STTHERESAF-KIS-2C3034	003571		P.O BOX 669-40200 KISII FAITH BASED DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0HOMA BAY LICENCED	t			2025-09-01 20:03:33.335+03	2025-09-01 20:03:33.335+03	2	1	\N	207
12524	Afya Research Africa-Mfangano Community Health Centre	AFYARESEAR-NAI-5F6009	007172		P.O BOX 20880-00202 NAIROBI HEALTH CENTRE Private LEVEL 3B 0HOMA BAY LICENCED	t			2025-09-01 20:03:34.776+03	2025-09-01 20:03:34.776+03	2	1	\N	194
12525	Okitta Nursing And Maternity Home	OKITTANURS-KIS-289891	000088		P.O BOX 4-40223 KADONGO KISUMU NURSING HOME Private LEVEL 3B 54HOMA BAY LICENCED	t			2025-09-01 20:03:36.834+03	2025-09-01 20:03:36.834+03	2	1	\N	198
12526	Port Florence Community Hospital Homa Bay	PORTFLOREN-KIS-D2FB39	003113		P.O BOX 3417-40100 KISUMU MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED	t			2025-09-01 20:03:38.381+03	2025-09-01 20:03:38.381+03	2	1	\N	198
12527	The Aga Khan Hospital Homabay	THEAGAKHAN-KIS-234D87	003667		P.O BOX 530-40100 KISUMU MEDICAL CENTRE Private LEVEL 3A 0HOMA BAY LICENCED	t			2025-09-01 20:03:38.484+03	2025-09-01 20:03:38.484+03	2	1	\N	198
12528	Watta Medical Clinic	WATTAMEDIC-MIG-C2B0D9	004299		P.O BOX 36-40400 SUNA - MIGORI MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED	t			2025-09-01 20:03:39.833+03	2025-09-01 20:03:39.833+03	2	1	\N	201
12529	Port Florence Community Hospital Ndhiwa	PORTFLOREN-KIS-E1AE55	006575		P.O BOX 3417-40100 KISUMU NURSING HOME Private LEVEL 3B 35HOMA BAY LICENCED	t			2025-09-01 20:03:41.529+03	2025-09-01 20:03:41.529+03	2	1	\N	198
12530	Katito Medical Centre-Mbita	KATITOMEDI-KIS-A1712C	015029		P.O BOX 1764-40100 KISUMU HOSPITAL LEVEL 4 Private LEVEL 4 75HOMA BAY LICENCED	t			2025-09-01 20:03:43.413+03	2025-09-01 20:03:43.413+03	2	1	\N	198
12531	Bliss Healthcare Ltd Homabay	BLISSHEALT-NAI-A95B23	015106		P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED	t			2025-09-01 20:03:44.758+03	2025-09-01 20:03:44.758+03	2	1	\N	194
12532	Tudor Healthcare Ltd-Sindo	TUDORHEALT-MOM-934089	015336		P.O BOX 91291-80100 MOMBASA NURSING HOME Private LEVEL 3B 35HOMA BAY LICENCED	t			2025-09-01 20:03:46.315+03	2025-09-01 20:03:46.315+03	2	1	\N	208
12533	Hawi Family Hospital	HAWIFAMILY-KIS-509185	015688		P.O BOX 1251-40100 KISUMU HOSPITAL LEVEL 4 Private LEVEL 4 120 HOMA BAY LICENCED	t			2025-09-01 20:03:47.863+03	2025-09-01 20:03:47.863+03	2	1	\N	198
12534	Manyatta Community Nursing Home	MANYATTACO-KIS-FDC0EF	017056		P.O BOX 1896-40100 KISUMU NURSING HOME Private LEVEL 3B 34HOMA BAY LICENCED	t			2025-09-01 20:03:49.634+03	2025-09-01 20:03:49.634+03	2	1	\N	198
12535	Nguono Medical Centre	NGUONOMEDI-KIS-021582	017797		P.O BOX 2155-40100 KISUMU MEDICAL CENTRE Private LEVEL 3A 40HOMA BAY LICENCED	t			2025-09-01 20:03:51.155+03	2025-09-01 20:03:51.155+03	2	1	\N	198
12536	Jatriz Medical Centre	JATRIZMEDI-BUN-749F7D	018338		P.O BOX 745-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED	t			2025-09-01 20:03:52.289+03	2025-09-01 20:03:52.289+03	2	1	\N	199
12537	Flo Dental Clinic	FLODENTALC-KIS-5212AD	018783		P.O BOX 1236-40100 KISUMU DENTAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED	t			2025-09-01 20:03:53.462+03	2025-09-01 20:03:53.462+03	2	1	\N	198
12538	Raksha International Medical Services Limited	RAKSHAINTE-NAI-F30F9E	018787		P.O BOX 8452-00200 NAIROBI HOSPITAL LEVEL 4 Private LEVEL 4 76HOMA BAY LICENCED	t			2025-09-01 20:03:54.819+03	2025-09-01 20:03:54.819+03	2	1	\N	194
12539	Equity Afia Homabay Medical Center	EQUITYAFIA-NAI-C83FF2	020857		P.O BOX 41693-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0HOMA BAY LICENCED	t			2025-09-01 20:03:56.628+03	2025-09-01 20:03:56.628+03	2	1	\N	194
12540	Rehema Hospice And Clinic Limited	REHEMAHOSP-KIS-D9E801	020861		P.O BOX 3072-40100 KISUMU NURSING HOME Private LEVEL 3B 19HOMA BAY LICENCED	t			2025-09-01 20:03:58.366+03	2025-09-01 20:03:58.366+03	2	1	\N	198
12541	Perisqure Medical Clinics And Laboratories	PERISQUREM-NAI-FD1128	018541		P.O BOX 997-00100 NAIROBI MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:00.409+03	2025-09-01 20:04:00.409+03	2	1	\N	194
12542	Isiolo Regional Hospital-Barracks	ISIOLOREGI-ISI-917DFC	GK-019265		P.O BOX 66- ISIOLO HOSPITAL LEVEL 4 Public LEVEL 4 80ISIOLO LICENCED	t			2025-09-01 20:04:02.695+03	2025-09-01 20:04:02.695+03	2	1	\N	209
12543	Aic Isiolo Dispensary	AICISIOLOD-ISI-E962FA	001102		P.O BOX 262-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:04.826+03	2025-09-01 20:04:04.826+03	2	1	\N	209
12544	A.C.K Isiolo Dispensary	ACKISIOLOD-ISI-EA94AF	001680		P.O BOX 110-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:05.099+03	2025-09-01 20:04:05.099+03	2	1	\N	209
12545	Archers Post Catholic Health Centre	ARCHERSPOS-ISI-9F7854	002967		P.O BOX 359-60300 ISIOLO FAITH-BASED BASIC CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3A 31ISIOLO LICENCED	t			2025-09-01 20:04:05.376+03	2025-09-01 20:04:05.376+03	2	1	\N	209
12546	Isiolo Catholic Dispensary	ISIOLOCATH-ISI-62D324	003111		P.O BOX 162-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:07.35+03	2025-09-01 20:04:07.35+03	2	1	\N	209
12547	St.John Paul Ii A Vi Matercare Hospital	STJOHNPAUL-ISI-D07949	003237		P.O BOX 340-60300 ISIOLO HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 40ISIOLO LICENCED	t			2025-09-01 20:04:08.791+03	2025-09-01 20:04:08.791+03	2	1	\N	209
12548	Camp Garba Catholic Dispensary	CAMPGARBAC-ISI-BF1910	003806		P.O BOX 319-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:10.547+03	2025-09-01 20:04:10.547+03	2	1	\N	209
12549	Catholic Dispensary Ngaremara	CATHOLICDI-ISI-A27212	003825		P.O BOX 232-60300 ISIOLO FAITH BASED DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:12.288+03	2025-09-01 20:04:12.288+03	2	1	\N	209
12550	Leparua Community Medical Clinic	LEPARUACOM-ISI-212080	001576		P.O BOX PRIV ATE BAG-60300 ISIOLO MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:14.141+03	2025-09-01 20:04:14.141+03	2	1	\N	209
12551	Pepo La Tumaini Jangwani Health Centre	PEPOLATUMA-ISI-6D5697	002316		P.O BOX 280-60300 ISIOLO MEDICAL CENTRE Private LEVEL 3A 0ISIOLO LICENCED	t			2025-09-01 20:04:16.304+03	2025-09-01 20:04:16.304+03	2	1	\N	209
12552	Iqra Medical Centre And Nursing Home	IQRAMEDICA-ISI-0C5379	002346		P.O BOX 131-60300 ISIOLO NURSING HOME Private LEVEL 3B 40ISIOLO LICENCED	t			2025-09-01 20:04:18.36+03	2025-09-01 20:04:18.36+03	2	1	\N	209
12553	Isiolo County Nursing Home	ISIOLOCOUN-ISI-4279BC	003103		P.O BOX 588- ISIOLO NURSING HOME Private LEVEL 3B 20ISIOLO LICENCED	t			2025-09-01 20:04:18.498+03	2025-09-01 20:04:18.498+03	2	1	\N	209
12554	Kulamawe Medical Services	KULAMAWEME-ISI-C15DAF	003829		P.O BOX 670-60300 ISIOLO MEDICAL CENTRE Private LEVEL 3A 12ISIOLO LICENCED	t			2025-09-01 20:04:19.746+03	2025-09-01 20:04:19.746+03	2	1	\N	209
12555	Down Town Medical Clinic	DOWNTOWNME-ISI-4AE0E7	003979		P.O BOX 247-60300 ISIOLO MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:21.565+03	2025-09-01 20:04:21.565+03	2	1	\N	209
12556	Healthpact Hospital	HEALTHPACT-ISI-DBA821	004130		P.O BOX 457-60300 ISIOLO HOSPITAL LEVEL 4 Private LEVEL 4 30ISIOLO LICENCED	t			2025-09-01 20:04:23.08+03	2025-09-01 20:04:23.08+03	2	1	\N	209
12557	Simba Clinic	SIMBACLINI-ISI-5285F5	004154		P.O BOX 782-60300 ISIOLO MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:24.343+03	2025-09-01 20:04:24.343+03	2	1	\N	209
12558	Waso Aipca Dispensary	WASOAIPCAD-ISI-38E538	004286		P.O BOX 727- ISIOLO DISPENSARY Private LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:24.466+03	2025-09-01 20:04:24.466+03	2	1	\N	209
12559	Almas Medical Services	ALMASMEDIC-ISI-CB8C0C	005732		P.O BOX 652-60300 ISIOLO NURSING HOME Private LEVEL 3B 18ISIOLO LICENCED	t			2025-09-01 20:04:26.127+03	2025-09-01 20:04:26.127+03	2	1	\N	209
12560	Elephant Dental Isiolo	ELEPHANTDE-ISI-31F8A1	005980		P.O BOX 821-60300 ISIOLO DENTAL CLINIC Private LEVEL 2 0ISIOLO LICENCED	t			2025-09-01 20:04:27.794+03	2025-09-01 20:04:27.794+03	2	1	\N	209
12561	Galaxy Hospital Limited	GALAXYHOSP-ISI-905AC0	006545		P.O BOX 674-60300 ISIOLO Hospital Level 5 Private LEVEL 5 70ISIOLO LICENCED	t			2025-09-01 20:04:29.288+03	2025-09-01 20:04:29.288+03	2	1	\N	209
\.


--
-- TOC entry 4102 (class 0 OID 67410)
-- Dependencies: 275
-- Data for Name: facility_contacts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facility_contacts (contact_id, contact_value, contact_person_name, is_primary, is_active, created_at, updated_at, contact_type_id, created_by, facility_id, updated_by) FROM stdin;
36608	+254700000000	Facility Manager	t	t	2025-09-01 19:56:33.902+03	2025-09-01 19:56:33.902+03	1	2	12201	\N
36609	info@baringocountyreferra.com	Information Desk	f	t	2025-09-01 19:56:33.909+03	2025-09-01 19:56:33.909+03	2	2	12201	\N
36610	P.O BOX 21-30400 KABARNET HOSPITAL LEVEL 4 Public LEVEL 4 100 BARINGO LICENCED		f	t	2025-09-01 19:56:33.916+03	2025-09-01 19:56:33.916+03	14	2	12201	\N
36611	+254700000000	Facility Manager	t	t	2025-09-01 19:56:35.261+03	2025-09-01 19:56:35.261+03	1	2	12202	\N
36612	info@eldamaravinesubcount.com	Information Desk	f	t	2025-09-01 19:56:35.27+03	2025-09-01 19:56:35.27+03	2	2	12202	\N
36613	P.O BOX 102-20103 ELDAMA RA VINE HOSPITAL LEVEL 4 Public LEVEL 4 120 BARINGO LICENCED		f	t	2025-09-01 19:56:35.278+03	2025-09-01 19:56:35.278+03	14	2	12202	\N
36614	+254700000000	Facility Manager	t	t	2025-09-01 19:56:37.324+03	2025-09-01 19:56:37.324+03	1	2	12203	\N
36615	info@mercymissionhospital.com	Information Desk	f	t	2025-09-01 19:56:37.331+03	2025-09-01 19:56:37.331+03	2	2	12203	\N
36616	P.O BOX 10-20103 ELDAMA RA VINE FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 110 BARINGO LICENCED		f	t	2025-09-01 19:56:37.353+03	2025-09-01 19:56:37.353+03	14	2	12203	\N
36617	+254700000000	Facility Manager	t	t	2025-09-01 19:56:37.782+03	2025-09-01 19:56:37.782+03	1	2	12204	\N
36618	info@kitabisidispensary.com	Information Desk	f	t	2025-09-01 19:56:37.79+03	2025-09-01 19:56:37.79+03	2	2	12204	\N
36619	P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:37.798+03	2025-09-01 19:56:37.798+03	14	2	12204	\N
36620	+254700000000	Facility Manager	t	t	2025-09-01 19:56:39.038+03	2025-09-01 19:56:39.038+03	1	2	12205	\N
36621	info@kibukehealthcentre.com	Information Desk	f	t	2025-09-01 19:56:39.044+03	2025-09-01 19:56:39.044+03	2	2	12205	\N
36622	P.O BOX 14-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 18BUNGOMA LICENCED		f	t	2025-09-01 19:56:39.051+03	2025-09-01 19:56:39.051+03	14	2	12205	\N
36623	+254700000000	Facility Manager	t	t	2025-09-01 19:56:39.102+03	2025-09-01 19:56:39.102+03	1	2	12206	\N
36624	info@muandahealthcentre.com	Information Desk	f	t	2025-09-01 19:56:39.109+03	2025-09-01 19:56:39.109+03	2	2	12206	\N
36625	P.O BOX 754-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 21BUNGOMA LICENCED		f	t	2025-09-01 19:56:39.116+03	2025-09-01 19:56:39.116+03	14	2	12206	\N
36626	+254700000000	Facility Manager	t	t	2025-09-01 19:56:40.464+03	2025-09-01 19:56:40.464+03	1	2	12207	\N
36627	info@nasiandahealthcentre.com	Information Desk	f	t	2025-09-01 19:56:40.471+03	2025-09-01 19:56:40.471+03	2	2	12207	\N
36628	P.O BOX 633-50200 BUNGOMA MEDICAL CLINIC Public LEVEL 2 6BUNGOMA LICENCED		f	t	2025-09-01 19:56:40.481+03	2025-09-01 19:56:40.481+03	14	2	12207	\N
36629	+254700000000	Facility Manager	t	t	2025-09-01 19:56:40.559+03	2025-09-01 19:56:40.559+03	1	2	12208	\N
36630	info@ranjedispensary.com	Information Desk	f	t	2025-09-01 19:56:40.57+03	2025-09-01 19:56:40.57+03	2	2	12208	\N
36631	P.O BOX 2495-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:40.581+03	2025-09-01 19:56:40.581+03	14	2	12208	\N
36632	+254700000000	Facility Manager	t	t	2025-09-01 19:56:40.618+03	2025-09-01 19:56:40.618+03	1	2	12209	\N
36633	info@kabulahealthcentre.com	Information Desk	f	t	2025-09-01 19:56:40.625+03	2025-09-01 19:56:40.625+03	2	2	12209	\N
36634	P.O BOX 14-50200 BUNGOMA HEALTH CENTRE Public LEVEL 3B 36BUNGOMA LICENCED		f	t	2025-09-01 19:56:40.632+03	2025-09-01 19:56:40.632+03	14	2	12209	\N
36635	+254700000000	Facility Manager	t	t	2025-09-01 19:56:40.674+03	2025-09-01 19:56:40.674+03	1	2	12210	\N
36636	info@bukokholodispensary.com	Information Desk	f	t	2025-09-01 19:56:40.689+03	2025-09-01 19:56:40.689+03	2	2	12210	\N
36637	P.O BOX 182-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:40.697+03	2025-09-01 19:56:40.697+03	14	2	12210	\N
36638	+254700000000	Facility Manager	t	t	2025-09-01 19:56:41.87+03	2025-09-01 19:56:41.87+03	1	2	12211	\N
36639	info@bungomag.kprisonheal.com	Information Desk	f	t	2025-09-01 19:56:41.877+03	2025-09-01 19:56:41.877+03	2	2	12211	\N
36640	P.O BOX 56-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 26BUNGOMA LICENCED		f	t	2025-09-01 19:56:41.884+03	2025-09-01 19:56:41.884+03	14	2	12211	\N
36641	+254700000000	Facility Manager	t	t	2025-09-01 19:56:43.375+03	2025-09-01 19:56:43.375+03	1	2	12212	\N
36642	info@mayanjahealthcentre.com	Information Desk	f	t	2025-09-01 19:56:43.381+03	2025-09-01 19:56:43.381+03	2	2	12212	\N
36643	P.O BOX 101-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 17BUNGOMA LICENCED		f	t	2025-09-01 19:56:43.388+03	2025-09-01 19:56:43.388+03	14	2	12212	\N
36644	+254700000000	Facility Manager	t	t	2025-09-01 19:56:43.435+03	2025-09-01 19:56:43.435+03	1	2	12213	\N
36645	info@webuyesubcountyhospi.com	Information Desk	f	t	2025-09-01 19:56:43.443+03	2025-09-01 19:56:43.443+03	2	2	12213	\N
36646	P.O BOX 25-50205 WEBUYE HOSPITAL LEVEL 4 Public LEVEL 4 217 BUNGOMA LICENCED		f	t	2025-09-01 19:56:43.451+03	2025-09-01 19:56:43.451+03	14	2	12213	\N
36647	+254700000000	Facility Manager	t	t	2025-09-01 19:56:44.717+03	2025-09-01 19:56:44.717+03	1	2	12214	\N
36648	info@bungomacountyreferra.com	Information Desk	f	t	2025-09-01 19:56:44.723+03	2025-09-01 19:56:44.723+03	2	2	12214	\N
36649	P.O BOX 14-50200 BUNGOMA HOSPITAL LEVEL 5 Public LEVEL 5 565 BUNGOMA LICENCED		f	t	2025-09-01 19:56:44.73+03	2025-09-01 19:56:44.73+03	14	2	12214	\N
36650	+254700000000	Facility Manager	t	t	2025-09-01 19:56:46.313+03	2025-09-01 19:56:46.313+03	1	2	12215	\N
36651	info@bumulasubcountyhospi.com	Information Desk	f	t	2025-09-01 19:56:46.321+03	2025-09-01 19:56:46.321+03	2	2	12215	\N
36652	P.O BOX 14-50200 BUNGOMA HOSPITAL LEVEL 4 Public LEVEL 4 30BUNGOMA LICENCED		f	t	2025-09-01 19:56:46.328+03	2025-09-01 19:56:46.328+03	14	2	12215	\N
36653	+254700000000	Facility Manager	t	t	2025-09-01 19:56:47.726+03	2025-09-01 19:56:47.726+03	1	2	12216	\N
36654	info@kimililisubcountyhos.com	Information Desk	f	t	2025-09-01 19:56:47.733+03	2025-09-01 19:56:47.733+03	2	2	12216	\N
36655	P.O BOX 490-50204 KIMILILI HOSPITAL LEVEL 4 Public LEVEL 4 180 BUNGOMA LICENCED		f	t	2025-09-01 19:56:47.739+03	2025-09-01 19:56:47.739+03	14	2	12216	\N
36656	+254700000000	Facility Manager	t	t	2025-09-01 19:56:49.391+03	2025-09-01 19:56:49.391+03	1	2	12217	\N
36657	info@kimaetihealthcentre.com	Information Desk	f	t	2025-09-01 19:56:49.398+03	2025-09-01 19:56:49.398+03	2	2	12217	\N
36658	P.O BOX 2313-50200 BUNGOMA HEALTH CENTRE Public LEVEL 3B 35BUNGOMA LICENCED		f	t	2025-09-01 19:56:49.406+03	2025-09-01 19:56:49.406+03	14	2	12217	\N
36659	+254700000000	Facility Manager	t	t	2025-09-01 19:56:49.462+03	2025-09-01 19:56:49.462+03	1	2	12218	\N
36660	info@mechimeruhealthcentr.com	Information Desk	f	t	2025-09-01 19:56:49.47+03	2025-09-01 19:56:49.47+03	2	2	12218	\N
36661	P.O BOX 14-50200 BUNGOMA HEALTH CENTRE Public LEVEL 3B 6BUNGOMA LICENCED		f	t	2025-09-01 19:56:49.477+03	2025-09-01 19:56:49.477+03	14	2	12218	\N
36662	+254700000000	Facility Manager	t	t	2025-09-01 19:56:49.528+03	2025-09-01 19:56:49.528+03	1	2	12219	\N
36663	info@bukembehealthcentre.com	Information Desk	f	t	2025-09-01 19:56:49.535+03	2025-09-01 19:56:49.535+03	2	2	12219	\N
36664	P.O BOX 14-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 20BUNGOMA LICENCED		f	t	2025-09-01 19:56:49.544+03	2025-09-01 19:56:49.544+03	14	2	12219	\N
36665	+254700000000	Facility Manager	t	t	2025-09-01 19:56:49.587+03	2025-09-01 19:56:49.587+03	1	2	12220	\N
36666	info@bisunudispensary.com	Information Desk	f	t	2025-09-01 19:56:49.594+03	2025-09-01 19:56:49.594+03	2	2	12220	\N
36667	P.O BOX 768-50200 BUNGOMA DISPENSARY Public LEVEL 2 5BUNGOMA LICENCED		f	t	2025-09-01 19:56:49.603+03	2025-09-01 19:56:49.604+03	14	2	12220	\N
36668	+254700000000	Facility Manager	t	t	2025-09-01 19:56:50.726+03	2025-09-01 19:56:50.726+03	1	2	12221	\N
36669	info@tuliengedispensary.com	Information Desk	f	t	2025-09-01 19:56:50.734+03	2025-09-01 19:56:50.734+03	2	2	12221	\N
36670	P.O BOX 122-50208 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:50.742+03	2025-09-01 19:56:50.742+03	14	2	12221	\N
36671	+254700000000	Facility Manager	t	t	2025-09-01 19:56:52.013+03	2025-09-01 19:56:52.013+03	1	2	12222	\N
36672	info@bulondohealthcentre.com	Information Desk	f	t	2025-09-01 19:56:52.02+03	2025-09-01 19:56:52.02+03	2	2	12222	\N
36673	P.O BOX 14-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 25BUNGOMA LICENCED		f	t	2025-09-01 19:56:52.026+03	2025-09-01 19:56:52.026+03	14	2	12222	\N
36674	+254700000000	Facility Manager	t	t	2025-09-01 19:56:52.088+03	2025-09-01 19:56:52.088+03	1	2	12223	\N
36675	info@nabukhisadispensary.com	Information Desk	f	t	2025-09-01 19:56:52.095+03	2025-09-01 19:56:52.096+03	2	2	12223	\N
36676	P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:52.103+03	2025-09-01 19:56:52.103+03	14	2	12223	\N
36677	+254700000000	Facility Manager	t	t	2025-09-01 19:56:53.361+03	2025-09-01 19:56:53.361+03	1	2	12224	\N
36678	info@myangahealthcentre.com	Information Desk	f	t	2025-09-01 19:56:53.402+03	2025-09-01 19:56:53.402+03	2	2	12224	\N
36679	P.O BOX 23194-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 15BUNGOMA LICENCED		f	t	2025-09-01 19:56:53.438+03	2025-09-01 19:56:53.438+03	14	2	12224	\N
36680	+254700000000	Facility Manager	t	t	2025-09-01 19:56:55.027+03	2025-09-01 19:56:55.027+03	1	2	12225	\N
36681	info@kamusindedispensary.com	Information Desk	f	t	2025-09-01 19:56:55.043+03	2025-09-01 19:56:55.043+03	2	2	12225	\N
36682	P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:55.059+03	2025-09-01 19:56:55.059+03	14	2	12225	\N
36683	+254700000000	Facility Manager	t	t	2025-09-01 19:56:56.255+03	2025-09-01 19:56:56.255+03	1	2	12226	\N
36684	info@kisawaiyidispensary.com	Information Desk	f	t	2025-09-01 19:56:56.269+03	2025-09-01 19:56:56.269+03	2	2	12226	\N
36685	P.O BOX 437-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:56.279+03	2025-09-01 19:56:56.279+03	14	2	12226	\N
36686	+254700000000	Facility Manager	t	t	2025-09-01 19:56:57.472+03	2025-09-01 19:56:57.472+03	1	2	12227	\N
36687	info@kipsabuladispensary.com	Information Desk	f	t	2025-09-01 19:56:57.496+03	2025-09-01 19:56:57.496+03	2	2	12227	\N
36688	P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:57.512+03	2025-09-01 19:56:57.512+03	14	2	12227	\N
36689	+254700000000	Facility Manager	t	t	2025-09-01 19:56:58.706+03	2025-09-01 19:56:58.706+03	1	2	12228	\N
36690	info@samoyadispensary.com	Information Desk	f	t	2025-09-01 19:56:58.714+03	2025-09-01 19:56:58.714+03	2	2	12228	\N
36691	P.O BOX 1835-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:58.722+03	2025-09-01 19:56:58.722+03	14	2	12228	\N
36692	+254700000000	Facility Manager	t	t	2025-09-01 19:56:59.809+03	2025-09-01 19:56:59.809+03	1	2	12229	\N
36693	info@butielidispensary.com	Information Desk	f	t	2025-09-01 19:56:59.824+03	2025-09-01 19:56:59.824+03	2	2	12229	\N
36694	P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:56:59.837+03	2025-09-01 19:56:59.837+03	14	2	12229	\N
36695	+254700000000	Facility Manager	t	t	2025-09-01 19:57:01.32+03	2025-09-01 19:57:01.32+03	1	2	12230	\N
36696	info@siritanyihealthcentr.com	Information Desk	f	t	2025-09-01 19:57:01.331+03	2025-09-01 19:57:01.331+03	2	2	12230	\N
36697	P.O BOX 437-50200 BUNGOMA BASIC HEALTH CENTRE Public LEVEL 3A 14BUNGOMA LICENCED		f	t	2025-09-01 19:57:01.346+03	2025-09-01 19:57:01.346+03	14	2	12230	\N
36698	+254700000000	Facility Manager	t	t	2025-09-01 19:57:02.591+03	2025-09-01 19:57:02.591+03	1	2	12231	\N
36699	info@kongitdispensary.com	Information Desk	f	t	2025-09-01 19:57:02.597+03	2025-09-01 19:57:02.597+03	2	2	12231	\N
36700	P.O BOX 49-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:02.604+03	2025-09-01 19:57:02.604+03	14	2	12231	\N
36701	+254700000000	Facility Manager	t	t	2025-09-01 19:57:04.324+03	2025-09-01 19:57:04.324+03	1	2	12232	\N
36702	info@makololwedispensary.com	Information Desk	f	t	2025-09-01 19:57:04.33+03	2025-09-01 19:57:04.33+03	2	2	12232	\N
36703	P.O BOX 49-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:04.338+03	2025-09-01 19:57:04.338+03	14	2	12232	\N
36704	+254700000000	Facility Manager	t	t	2025-09-01 19:57:05.96+03	2025-09-01 19:57:05.96+03	1	2	12233	\N
36705	info@makungadispensary.com	Information Desk	f	t	2025-09-01 19:57:05.969+03	2025-09-01 19:57:05.969+03	2	2	12233	\N
36706	P.O BOX 14-50200 BUNGOMA DISPENSARY Public LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:05.977+03	2025-09-01 19:57:05.977+03	14	2	12233	\N
36707	+254700000000	Facility Manager	t	t	2025-09-01 19:57:07.875+03	2025-09-01 19:57:07.875+03	1	2	12234	\N
36708	info@namirembedispensary.com	Information Desk	f	t	2025-09-01 19:57:07.884+03	2025-09-01 19:57:07.884+03	2	2	12234	\N
36709	P.O BOX 170-50200 BUNGOMA DISPENSARY Public LEVEL 2 6BUNGOMA LICENCED		f	t	2025-09-01 19:57:07.892+03	2025-09-01 19:57:07.892+03	14	2	12234	\N
36710	+254700000000	Facility Manager	t	t	2025-09-01 19:57:09.066+03	2025-09-01 19:57:09.066+03	1	2	12235	\N
36711	info@fatherslovefoundatio.com	Information Desk	f	t	2025-09-01 19:57:09.073+03	2025-09-01 19:57:09.073+03	2	2	12235	\N
36712	P.O BOX 1202-50200 BUNGOMA DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:09.08+03	2025-09-01 19:57:09.08+03	14	2	12235	\N
36713	+254700000000	Facility Manager	t	t	2025-09-01 19:57:10.532+03	2025-09-01 19:57:10.532+03	1	2	12236	\N
36714	info@missionofmercyhospit.com	Information Desk	f	t	2025-09-01 19:57:10.542+03	2025-09-01 19:57:10.542+03	2	2	12236	\N
36715	P.O BOX 1429-50200 BUNGOMA MISSION HOSPITAL LEVEL 3 FAITH BASED ORGANIZATION (FBO) LEVEL 3A 35BUNGOMA LICENCED		f	t	2025-09-01 19:57:10.549+03	2025-09-01 19:57:10.549+03	14	2	12236	\N
36716	+254700000000	Facility Manager	t	t	2025-09-01 19:57:10.608+03	2025-09-01 19:57:10.608+03	1	2	12237	\N
36717	info@stanthonyskibabiihea.com	Information Desk	f	t	2025-09-01 19:57:10.617+03	2025-09-01 19:57:10.617+03	2	2	12237	\N
36718	P.O BOX 512-5200 BUNGOMA HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 24BUNGOMA LICENCED		f	t	2025-09-01 19:57:10.625+03	2025-09-01 19:57:10.626+03	14	2	12237	\N
36719	+254700000000	Facility Manager	t	t	2025-09-01 19:57:12.212+03	2025-09-01 19:57:12.212+03	1	2	12238	\N
36720	info@st.damianomissionhos.com	Information Desk	f	t	2025-09-01 19:57:12.219+03	2025-09-01 19:57:12.219+03	2	2	12238	\N
36721	P.O BOX 1769-50200 BUNGOMA FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 80BUNGOMA LICENCED		f	t	2025-09-01 19:57:12.226+03	2025-09-01 19:57:12.226+03	14	2	12238	\N
36722	+254700000000	Facility Manager	t	t	2025-09-01 19:57:13.776+03	2025-09-01 19:57:13.776+03	1	2	12239	\N
36723	info@ackdr.pikeropermedic.com	Information Desk	f	t	2025-09-01 19:57:13.792+03	2025-09-01 19:57:13.792+03	2	2	12239	\N
36724	P.O BOX 2392-50200 BUNGOMA FAITH-BASED BASIC CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3A 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:13.809+03	2025-09-01 19:57:13.809+03	14	2	12239	\N
36725	+254700000000	Facility Manager	t	t	2025-09-01 19:57:15.28+03	2025-09-01 19:57:15.28+03	1	2	12240	\N
36726	info@carmeldispensarykimw.com	Information Desk	f	t	2025-09-01 19:57:15.287+03	2025-09-01 19:57:15.287+03	2	2	12240	\N
36727	P.O BOX 1658-50200 BUNGOMA DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:15.293+03	2025-09-01 19:57:15.293+03	14	2	12240	\N
36728	+254700000000	Facility Manager	t	t	2025-09-01 19:57:16.735+03	2025-09-01 19:57:16.735+03	1	2	12241	\N
36729	info@newelgonviewmedicalc.com	Information Desk	f	t	2025-09-01 19:57:16.741+03	2025-09-01 19:57:16.741+03	2	2	12241	\N
36730	P.O BOX 1747-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 64BUNGOMA LICENCED		f	t	2025-09-01 19:57:16.747+03	2025-09-01 19:57:16.747+03	14	2	12241	\N
36731	+254700000000	Facility Manager	t	t	2025-09-01 19:57:18.869+03	2025-09-01 19:57:18.869+03	1	2	12242	\N
36732	info@machwelefriendsdispe.com	Information Desk	f	t	2025-09-01 19:57:18.882+03	2025-09-01 19:57:18.882+03	2	2	12242	\N
36733	P.O BOX 1463-50200 BUNGOMA FAITH BASED DISPENSARY Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:18.898+03	2025-09-01 19:57:18.898+03	14	2	12242	\N
36734	+254700000000	Facility Manager	t	t	2025-09-01 19:57:20.564+03	2025-09-01 19:57:20.564+03	1	2	12243	\N
36735	info@nzoiamedicalcentre.com	Information Desk	f	t	2025-09-01 19:57:20.571+03	2025-09-01 19:57:20.571+03	2	2	12243	\N
36736	P.O BOX 471-50200 BUNGOMA NURSING HOME Private LEVEL 3B 75BUNGOMA LICENCED		f	t	2025-09-01 19:57:20.581+03	2025-09-01 19:57:20.581+03	14	2	12243	\N
36737	+254700000000	Facility Manager	t	t	2025-09-01 19:57:20.649+03	2025-09-01 19:57:20.649+03	1	2	12244	\N
36738	info@theagakhanhospitalbu.com	Information Desk	f	t	2025-09-01 19:57:20.674+03	2025-09-01 19:57:20.674+03	2	2	12244	\N
36739	P.O BOX 530-40100 KISUMU MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:20.688+03	2025-09-01 19:57:20.688+03	14	2	12244	\N
36740	+254700000000	Facility Manager	t	t	2025-09-01 19:57:22.046+03	2025-09-01 19:57:22.046+03	1	2	12245	\N
36741	info@bungomawesthospital.com	Information Desk	f	t	2025-09-01 19:57:22.052+03	2025-09-01 19:57:22.052+03	2	2	12245	\N
36742	P.O BOX 152-50200 BUNGOMA HOSPITAL LEVEL 5 Private LEVEL 5 122 BUNGOMA LICENCED		f	t	2025-09-01 19:57:22.059+03	2025-09-01 19:57:22.059+03	14	2	12245	\N
36743	+254700000000	Facility Manager	t	t	2025-09-01 19:57:23.75+03	2025-09-01 19:57:23.75+03	1	2	12246	\N
36744	info@khalabamedicalservic.com	Information Desk	f	t	2025-09-01 19:57:23.758+03	2025-09-01 19:57:23.758+03	2	2	12246	\N
36745	P.O BOX 2211-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 27BUNGOMA LICENCED		f	t	2025-09-01 19:57:23.766+03	2025-09-01 19:57:23.766+03	14	2	12246	\N
36746	+254700000000	Facility Manager	t	t	2025-09-01 19:57:23.82+03	2025-09-01 19:57:23.82+03	1	2	12247	\N
36747	info@bungomawemacentre.com	Information Desk	f	t	2025-09-01 19:57:23.827+03	2025-09-01 19:57:23.827+03	2	2	12247	\N
36748	P.O BOX 2270-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:23.839+03	2025-09-01 19:57:23.839+03	14	2	12247	\N
36749	+254700000000	Facility Manager	t	t	2025-09-01 19:57:25.157+03	2025-09-01 19:57:25.157+03	1	2	12248	\N
36750	info@st.jamesopticals.com	Information Desk	f	t	2025-09-01 19:57:25.164+03	2025-09-01 19:57:25.164+03	2	2	12248	\N
36751	P.O BOX 2141-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:25.171+03	2025-09-01 19:57:25.171+03	14	2	12248	\N
36752	+254700000000	Facility Manager	t	t	2025-09-01 19:57:26.47+03	2025-09-01 19:57:26.47+03	1	2	12249	\N
36753	info@kanduyihealthcentre.com	Information Desk	f	t	2025-09-01 19:57:26.48+03	2025-09-01 19:57:26.48+03	2	2	12249	\N
36754	P.O BOX 536-50200 BUNGOMA HEALTH CENTRE Private LEVEL 3B 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:26.489+03	2025-09-01 19:57:26.489+03	14	2	12249	\N
36755	+254700000000	Facility Manager	t	t	2025-09-01 19:57:28.147+03	2025-09-01 19:57:28.147+03	1	2	12250	\N
36756	info@trinityopticalsltd.com	Information Desk	f	t	2025-09-01 19:57:28.153+03	2025-09-01 19:57:28.153+03	2	2	12250	\N
36757	P.O BOX 2397-50200 BUNGOMA EYE CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:28.16+03	2025-09-01 19:57:28.16+03	14	2	12250	\N
36758	+254700000000	Facility Manager	t	t	2025-09-01 19:57:29.732+03	2025-09-01 19:57:29.732+03	1	2	12251	\N
36759	info@blisshealthcarelimit.com	Information Desk	f	t	2025-09-01 19:57:29.739+03	2025-09-01 19:57:29.739+03	2	2	12251	\N
36760	P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:29.747+03	2025-09-01 19:57:29.747+03	14	2	12251	\N
36761	+254700000000	Facility Manager	t	t	2025-09-01 19:57:31.181+03	2025-09-01 19:57:31.181+03	1	2	12252	\N
36762	info@blisshealthcareltdwe.com	Information Desk	f	t	2025-09-01 19:57:31.19+03	2025-09-01 19:57:31.19+03	2	2	12252	\N
36763	P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:31.202+03	2025-09-01 19:57:31.202+03	14	2	12252	\N
36764	+254700000000	Facility Manager	t	t	2025-09-01 19:57:32.576+03	2025-09-01 19:57:32.576+03	1	2	12253	\N
36765	info@nabualahospital.com	Information Desk	f	t	2025-09-01 19:57:32.583+03	2025-09-01 19:57:32.583+03	2	2	12253	\N
36766	P.O BOX 1001-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 120 BUNGOMA LICENCED		f	t	2025-09-01 19:57:32.591+03	2025-09-01 19:57:32.591+03	14	2	12253	\N
36767	+254700000000	Facility Manager	t	t	2025-09-01 19:57:33.625+03	2025-09-01 19:57:33.625+03	1	2	12254	\N
36768	info@fountainhealthcarelt.com	Information Desk	f	t	2025-09-01 19:57:33.632+03	2025-09-01 19:57:33.632+03	2	2	12254	\N
36769	P.O BOX 1596-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 26BUNGOMA LICENCED		f	t	2025-09-01 19:57:33.64+03	2025-09-01 19:57:33.64+03	14	2	12254	\N
36770	+254700000000	Facility Manager	t	t	2025-09-01 19:57:35.193+03	2025-09-01 19:57:35.193+03	1	2	12255	\N
36771	info@mpelimedicalcentre.com	Information Desk	f	t	2025-09-01 19:57:35.203+03	2025-09-01 19:57:35.203+03	2	2	12255	\N
36772	P.O BOX 1699-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 30BUNGOMA LICENCED		f	t	2025-09-01 19:57:35.211+03	2025-09-01 19:57:35.211+03	14	2	12255	\N
36773	+254700000000	Facility Manager	t	t	2025-09-01 19:57:36.158+03	2025-09-01 19:57:36.158+03	1	2	12256	\N
36774	info@lifecarehospitalsbun.com	Information Desk	f	t	2025-09-01 19:57:36.165+03	2025-09-01 19:57:36.165+03	2	2	12256	\N
36775	P.O BOX 22476-00505 NAIROBI Hospital Level 5 Private LEVEL 5 105 BUNGOMA LICENCED		f	t	2025-09-01 19:57:36.177+03	2025-09-01 19:57:36.177+03	14	2	12256	\N
36776	+254700000000	Facility Manager	t	t	2025-09-01 19:57:37.848+03	2025-09-01 19:57:37.848+03	1	2	12257	\N
36777	info@zionmedicalcentrebun.com	Information Desk	f	t	2025-09-01 19:57:37.855+03	2025-09-01 19:57:37.855+03	2	2	12257	\N
36778	P.O BOX 1561-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 61BUNGOMA LICENCED		f	t	2025-09-01 19:57:37.864+03	2025-09-01 19:57:37.864+03	14	2	12257	\N
36779	+254700000000	Facility Manager	t	t	2025-09-01 19:57:39.209+03	2025-09-01 19:57:39.209+03	1	2	12258	\N
36780	info@koryfamilyhospitalki.com	Information Desk	f	t	2025-09-01 19:57:39.216+03	2025-09-01 19:57:39.216+03	2	2	12258	\N
36781	P.O BOX 1977-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 74BUNGOMA LICENCED		f	t	2025-09-01 19:57:39.222+03	2025-09-01 19:57:39.222+03	14	2	12258	\N
36782	+254700000000	Facility Manager	t	t	2025-09-01 19:57:40.901+03	2025-09-01 19:57:40.901+03	1	2	12259	\N
36783	info@bungomawesthospitalt.com	Information Desk	f	t	2025-09-01 19:57:40.913+03	2025-09-01 19:57:40.913+03	2	2	12259	\N
36784	P.O BOX 152-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:40.92+03	2025-09-01 19:57:40.92+03	14	2	12259	\N
36785	+254700000000	Facility Manager	t	t	2025-09-01 19:57:43.06+03	2025-09-01 19:57:43.06+03	1	2	12260	\N
36786	info@brilliandoctorsplaza.com	Information Desk	f	t	2025-09-01 19:57:43.072+03	2025-09-01 19:57:43.072+03	2	2	12260	\N
36787	P.O BOX 5881-30100 ELDORET NURSING HOME Private LEVEL 3B 25BUNGOMA LICENCED		f	t	2025-09-01 19:57:43.081+03	2025-09-01 19:57:43.081+03	14	2	12260	\N
36788	+254700000000	Facility Manager	t	t	2025-09-01 19:57:44.623+03	2025-09-01 19:57:44.623+03	1	2	12261	\N
36789	info@mercalhealthcarebuke.com	Information Desk	f	t	2025-09-01 19:57:44.63+03	2025-09-01 19:57:44.63+03	2	2	12261	\N
36790	P.O BOX 244-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:44.636+03	2025-09-01 19:57:44.636+03	14	2	12261	\N
36791	+254700000000	Facility Manager	t	t	2025-09-01 19:57:46.105+03	2025-09-01 19:57:46.105+03	1	2	12262	\N
36792	info@thedawamedshospitall.com	Information Desk	f	t	2025-09-01 19:57:46.112+03	2025-09-01 19:57:46.112+03	2	2	12262	\N
36793	P.O BOX 70-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 80BUNGOMA LICENCED		f	t	2025-09-01 19:57:46.119+03	2025-09-01 19:57:46.119+03	14	2	12262	\N
36794	+254700000000	Facility Manager	t	t	2025-09-01 19:57:47.764+03	2025-09-01 19:57:47.764+03	1	2	12263	\N
36795	info@chrizahmedicalclinic.com	Information Desk	f	t	2025-09-01 19:57:47.775+03	2025-09-01 19:57:47.775+03	2	2	12263	\N
36796	P.O BOX 911-50100 KAKAMEGA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:47.786+03	2025-09-01 19:57:47.786+03	14	2	12263	\N
36797	+254700000000	Facility Manager	t	t	2025-09-01 19:57:50.569+03	2025-09-01 19:57:50.569+03	1	2	12264	\N
36798	info@globalhomecareltdmed.com	Information Desk	f	t	2025-09-01 19:57:50.581+03	2025-09-01 19:57:50.581+03	2	2	12264	\N
36799	P.O BOX 181-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:50.605+03	2025-09-01 19:57:50.605+03	14	2	12264	\N
36800	+254700000000	Facility Manager	t	t	2025-09-01 19:57:52.421+03	2025-09-01 19:57:52.421+03	1	2	12265	\N
36801	info@springwellmedicalcli.com	Information Desk	f	t	2025-09-01 19:57:52.428+03	2025-09-01 19:57:52.428+03	2	2	12265	\N
36802	P.O BOX 4640-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:52.436+03	2025-09-01 19:57:52.436+03	14	2	12265	\N
36803	+254700000000	Facility Manager	t	t	2025-09-01 19:57:54.225+03	2025-09-01 19:57:54.225+03	1	2	12266	\N
36804	info@healridgemedicalcent.com	Information Desk	f	t	2025-09-01 19:57:54.247+03	2025-09-01 19:57:54.247+03	2	2	12266	\N
36805	P.O BOX 552-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:54.257+03	2025-09-01 19:57:54.257+03	14	2	12266	\N
36806	+254700000000	Facility Manager	t	t	2025-09-01 19:57:55.525+03	2025-09-01 19:57:55.525+03	1	2	12267	\N
36807	info@mangshealthcareclini.com	Information Desk	f	t	2025-09-01 19:57:55.533+03	2025-09-01 19:57:55.533+03	2	2	12267	\N
36808	P.O BOX 2212-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:57:55.542+03	2025-09-01 19:57:55.542+03	14	2	12267	\N
36809	+254700000000	Facility Manager	t	t	2025-09-01 19:57:57.229+03	2025-09-01 19:57:57.229+03	1	2	12268	\N
36810	info@wandamedicalcentre.com	Information Desk	f	t	2025-09-01 19:57:57.236+03	2025-09-01 19:57:57.237+03	2	2	12268	\N
36811	P.O BOX 1977-50200 BUNGOMA NURSING HOME Private LEVEL 3B 22BUNGOMA LICENCED		f	t	2025-09-01 19:57:57.244+03	2025-09-01 19:57:57.244+03	14	2	12268	\N
36812	+254700000000	Facility Manager	t	t	2025-09-01 19:57:58.444+03	2025-09-01 19:57:58.444+03	1	2	12269	\N
36813	info@thehopkinscrescentho.com	Information Desk	f	t	2025-09-01 19:57:58.452+03	2025-09-01 19:57:58.452+03	2	2	12269	\N
36814	P.O BOX 2338-50200 BUNGOMA HOSPITAL LEVEL 4 Private LEVEL 4 60BUNGOMA LICENCED		f	t	2025-09-01 19:57:58.46+03	2025-09-01 19:57:58.46+03	14	2	12269	\N
36815	+254700000000	Facility Manager	t	t	2025-09-01 19:58:00.563+03	2025-09-01 19:58:00.563+03	1	2	12270	\N
36816	info@bungomachildrensclin.com	Information Desk	f	t	2025-09-01 19:58:00.569+03	2025-09-01 19:58:00.569+03	2	2	12270	\N
36817	P.O BOX 1125-30100 ELDORET MEDICAL CENTRE Private LEVEL 3A 10BUNGOMA LICENCED		f	t	2025-09-01 19:58:00.577+03	2025-09-01 19:58:00.577+03	14	2	12270	\N
36818	+254700000000	Facility Manager	t	t	2025-09-01 19:58:02.357+03	2025-09-01 19:58:02.357+03	1	2	12271	\N
36819	info@saintjudethaddeomaba.com	Information Desk	f	t	2025-09-01 19:58:02.365+03	2025-09-01 19:58:02.365+03	2	2	12271	\N
36820	P.O BOX 997-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:02.371+03	2025-09-01 19:58:02.371+03	14	2	12271	\N
36821	+254700000000	Facility Manager	t	t	2025-09-01 19:58:04.005+03	2025-09-01 19:58:04.005+03	1	2	12272	\N
36822	info@bucknerfamilyhopecli.com	Information Desk	f	t	2025-09-01 19:58:04.013+03	2025-09-01 19:58:04.013+03	2	2	12272	\N
36823	P.O BOX 2520-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:04.02+03	2025-09-01 19:58:04.02+03	14	2	12272	\N
36824	+254700000000	Facility Manager	t	t	2025-09-01 19:58:05.88+03	2025-09-01 19:58:05.88+03	1	2	12273	\N
36825	info@oasisdoctorsplazaweb.com	Information Desk	f	t	2025-09-01 19:58:05.887+03	2025-09-01 19:58:05.887+03	2	2	12273	\N
36826	P.O BOX 174-40400 MIGORI HOSPITAL LEVEL 4 Private LEVEL 4 45BUNGOMA LICENCED		f	t	2025-09-01 19:58:05.894+03	2025-09-01 19:58:05.894+03	14	2	12273	\N
36827	+254700000000	Facility Manager	t	t	2025-09-01 19:58:07.615+03	2025-09-01 19:58:07.615+03	1	2	12274	\N
36828	info@thedawamedshospitall.com	Information Desk	f	t	2025-09-01 19:58:07.622+03	2025-09-01 19:58:07.622+03	2	2	12274	\N
36829	P.O BOX 2448-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 25BUNGOMA LICENCED		f	t	2025-09-01 19:58:07.629+03	2025-09-01 19:58:07.629+03	14	2	12274	\N
36830	+254700000000	Facility Manager	t	t	2025-09-01 19:58:09.174+03	2025-09-01 19:58:09.174+03	1	2	12275	\N
36831	info@bungomaadorahclinic.com	Information Desk	f	t	2025-09-01 19:58:09.181+03	2025-09-01 19:58:09.181+03	2	2	12275	\N
36832	P.O BOX 15-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:09.188+03	2025-09-01 19:58:09.188+03	14	2	12275	\N
36833	+254700000000	Facility Manager	t	t	2025-09-01 19:58:10.818+03	2025-09-01 19:58:10.818+03	1	2	12276	\N
36834	info@afyaspaceconsultancy.com	Information Desk	f	t	2025-09-01 19:58:10.825+03	2025-09-01 19:58:10.825+03	2	2	12276	\N
36835	P.O BOX 545-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:10.833+03	2025-09-01 19:58:10.833+03	14	2	12276	\N
36836	+254700000000	Facility Manager	t	t	2025-09-01 19:58:12.759+03	2025-09-01 19:58:12.759+03	1	2	12277	\N
36837	info@rozajemmedicalcentre.com	Information Desk	f	t	2025-09-01 19:58:12.768+03	2025-09-01 19:58:12.768+03	2	2	12277	\N
36838	P.O BOX 352-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:12.785+03	2025-09-01 19:58:12.785+03	14	2	12277	\N
36839	+254700000000	Facility Manager	t	t	2025-09-01 19:58:14.076+03	2025-09-01 19:58:14.076+03	1	2	12278	\N
36840	info@alihsaanhealthcentre.com	Information Desk	f	t	2025-09-01 19:58:14.086+03	2025-09-01 19:58:14.086+03	2	2	12278	\N
36841	P.O BOX 11-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:14.096+03	2025-09-01 19:58:14.096+03	14	2	12278	\N
36842	+254700000000	Facility Manager	t	t	2025-09-01 19:58:15.746+03	2025-09-01 19:58:15.746+03	1	2	12279	\N
36843	info@connectionhealthserv.com	Information Desk	f	t	2025-09-01 19:58:15.753+03	2025-09-01 19:58:15.753+03	2	2	12279	\N
36844	P.O BOX 14-50200 BUNGOMA NURSING HOME Private LEVEL 3B 36BUNGOMA LICENCED		f	t	2025-09-01 19:58:15.761+03	2025-09-01 19:58:15.761+03	14	2	12279	\N
36845	+254700000000	Facility Manager	t	t	2025-09-01 19:58:17.369+03	2025-09-01 19:58:17.369+03	1	2	12280	\N
36846	info@st.paulskibabiittcme.com	Information Desk	f	t	2025-09-01 19:58:17.376+03	2025-09-01 19:58:17.376+03	2	2	12280	\N
36847	P.O BOX 931-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:17.385+03	2025-09-01 19:58:17.385+03	14	2	12280	\N
36848	+254700000000	Facility Manager	t	t	2025-09-01 19:58:19.079+03	2025-09-01 19:58:19.079+03	1	2	12281	\N
36849	info@kimwangamedicalcentr.com	Information Desk	f	t	2025-09-01 19:58:19.088+03	2025-09-01 19:58:19.088+03	2	2	12281	\N
36850	P.O BOX 2262-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:19.095+03	2025-09-01 19:58:19.095+03	14	2	12281	\N
36851	+254700000000	Facility Manager	t	t	2025-09-01 19:58:20.383+03	2025-09-01 19:58:20.383+03	1	2	12282	\N
36852	info@samaritaneyeretinace.com	Information Desk	f	t	2025-09-01 19:58:20.389+03	2025-09-01 19:58:20.389+03	2	2	12282	\N
36853	P.O BOX 63- BUNGOMA MEDICAL CENTRE Private LEVEL 3A 15BUNGOMA LICENCED		f	t	2025-09-01 19:58:20.396+03	2025-09-01 19:58:20.396+03	14	2	12282	\N
36854	+254700000000	Facility Manager	t	t	2025-09-01 19:58:22.202+03	2025-09-01 19:58:22.202+03	1	2	12283	\N
36855	info@transelgonhealthcare.com	Information Desk	f	t	2025-09-01 19:58:22.209+03	2025-09-01 19:58:22.209+03	2	2	12283	\N
36856	P.O BOX 19- BUNGOMA MEDICAL CENTRE Private LEVEL 3A 15BUNGOMA LICENCED		f	t	2025-09-01 19:58:22.216+03	2025-09-01 19:58:22.216+03	14	2	12283	\N
36857	+254700000000	Facility Manager	t	t	2025-09-01 19:58:23.894+03	2025-09-01 19:58:23.894+03	1	2	12284	\N
36858	info@morimedmedicalclinic.com	Information Desk	f	t	2025-09-01 19:58:23.902+03	2025-09-01 19:58:23.902+03	2	2	12284	\N
36859	P.O BOX 1474-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:23.91+03	2025-09-01 19:58:23.91+03	14	2	12284	\N
36860	+254700000000	Facility Manager	t	t	2025-09-01 19:58:25.699+03	2025-09-01 19:58:25.699+03	1	2	12285	\N
36861	info@melitamedicalcenter.com	Information Desk	f	t	2025-09-01 19:58:25.709+03	2025-09-01 19:58:25.709+03	2	2	12285	\N
36862	P.O BOX 2552-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:25.726+03	2025-09-01 19:58:25.726+03	14	2	12285	\N
36863	+254700000000	Facility Manager	t	t	2025-09-01 19:58:27.301+03	2025-09-01 19:58:27.301+03	1	2	12286	\N
36864	info@bungomadentaleyecare.com	Information Desk	f	t	2025-09-01 19:58:27.31+03	2025-09-01 19:58:27.31+03	2	2	12286	\N
36865	P.O BOX 67-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:27.318+03	2025-09-01 19:58:27.318+03	14	2	12286	\N
36866	+254700000000	Facility Manager	t	t	2025-09-01 19:58:29.116+03	2025-09-01 19:58:29.116+03	1	2	12287	\N
36867	info@elephantdentallimite.com	Information Desk	f	t	2025-09-01 19:58:29.123+03	2025-09-01 19:58:29.123+03	2	2	12287	\N
36868	P.O BOX --- BUNGOMA DENTAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:29.132+03	2025-09-01 19:58:29.132+03	14	2	12287	\N
36869	+254700000000	Facility Manager	t	t	2025-09-01 19:58:30.626+03	2025-09-01 19:58:30.626+03	1	2	12288	\N
36870	info@equityafialimitedbun.com	Information Desk	f	t	2025-09-01 19:58:30.633+03	2025-09-01 19:58:30.633+03	2	2	12288	\N
36871	P.O BOX 42752-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:30.64+03	2025-09-01 19:58:30.64+03	14	2	12288	\N
36872	+254700000000	Facility Manager	t	t	2025-09-01 19:58:32.355+03	2025-09-01 19:58:32.355+03	1	2	12289	\N
36873	info@elianeroyalhospitall.com	Information Desk	f	t	2025-09-01 19:58:32.368+03	2025-09-01 19:58:32.368+03	2	2	12289	\N
36874	P.O BOX 2211-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 30BUNGOMA LICENCED		f	t	2025-09-01 19:58:32.375+03	2025-09-01 19:58:32.375+03	14	2	12289	\N
36875	+254700000000	Facility Manager	t	t	2025-09-01 19:58:33.679+03	2025-09-01 19:58:33.679+03	1	2	12290	\N
36876	info@raciahospital.com	Information Desk	f	t	2025-09-01 19:58:33.686+03	2025-09-01 19:58:33.686+03	2	2	12290	\N
36877	P.O BOX 2495-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:33.695+03	2025-09-01 19:58:33.695+03	14	2	12290	\N
36878	+254700000000	Facility Manager	t	t	2025-09-01 19:58:34.79+03	2025-09-01 19:58:34.79+03	1	2	12291	\N
36879	info@chadmedicalcentre.com	Information Desk	f	t	2025-09-01 19:58:34.797+03	2025-09-01 19:58:34.797+03	2	2	12291	\N
36880	P.O BOX 924-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:34.804+03	2025-09-01 19:58:34.804+03	14	2	12291	\N
36881	+254700000000	Facility Manager	t	t	2025-09-01 19:58:36.211+03	2025-09-01 19:58:36.211+03	1	2	12292	\N
36882	info@myangamedicalclinic.com	Information Desk	f	t	2025-09-01 19:58:36.218+03	2025-09-01 19:58:36.218+03	2	2	12292	\N
36883	P.O BOX 571-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:36.225+03	2025-09-01 19:58:36.225+03	14	2	12292	\N
36884	+254700000000	Facility Manager	t	t	2025-09-01 19:58:37.706+03	2025-09-01 19:58:37.706+03	1	2	12293	\N
36885	info@olympiamedicalcentre.com	Information Desk	f	t	2025-09-01 19:58:37.716+03	2025-09-01 19:58:37.716+03	2	2	12293	\N
36886	P.O BOX 1699-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:37.723+03	2025-09-01 19:58:37.723+03	14	2	12293	\N
36887	+254700000000	Facility Manager	t	t	2025-09-01 19:58:38.841+03	2025-09-01 19:58:38.841+03	1	2	12294	\N
36888	info@nzoiasugarcompany.com	Information Desk	f	t	2025-09-01 19:58:38.851+03	2025-09-01 19:58:38.851+03	2	2	12294	\N
36889	P.O BOX 285-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0BUNGOMA LICENCED		f	t	2025-09-01 19:58:38.858+03	2025-09-01 19:58:38.858+03	14	2	12294	\N
36890	+254700000000	Facility Manager	t	t	2025-09-01 19:58:40.316+03	2025-09-01 19:58:40.316+03	1	2	12295	\N
36891	info@edesamedicarebungoma.com	Information Desk	f	t	2025-09-01 19:58:40.328+03	2025-09-01 19:58:40.328+03	2	2	12295	\N
36892	P.O BOX 519-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 8BUNGOMA LICENCED		f	t	2025-09-01 19:58:40.342+03	2025-09-01 19:58:40.342+03	14	2	12295	\N
36893	+254700000000	Facility Manager	t	t	2025-09-01 19:58:41.785+03	2025-09-01 19:58:41.785+03	1	2	12296	\N
36894	info@yourfamilycfwcommuni.com	Information Desk	f	t	2025-09-01 19:58:41.793+03	2025-09-01 19:58:41.793+03	2	2	12296	\N
36895	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:41.801+03	2025-09-01 19:58:41.801+03	14	2	12296	\N
36896	+254700000000	Facility Manager	t	t	2025-09-01 19:58:43.619+03	2025-09-01 19:58:43.619+03	1	2	12297	\N
36897	info@busiacountyreferralh.com	Information Desk	f	t	2025-09-01 19:58:43.627+03	2025-09-01 19:58:43.627+03	2	2	12297	\N
36898	P.O BOX 87-50400 BUSIA HOSPITAL LEVEL 4 Public LEVEL 4 149 BUSIA LICENCED		f	t	2025-09-01 19:58:43.635+03	2025-09-01 19:58:43.635+03	14	2	12297	\N
36899	+254700000000	Facility Manager	t	t	2025-09-01 19:58:45.072+03	2025-09-01 19:58:45.072+03	1	2	12298	\N
36900	info@karitrcalupehospital.com	Information Desk	f	t	2025-09-01 19:58:45.079+03	2025-09-01 19:58:45.079+03	2	2	12298	\N
36901	P.O BOX 399-50400 BUSIA HEALTH CENTRE Public LEVEL 3B 12BUSIA LICENCED		f	t	2025-09-01 19:58:45.088+03	2025-09-01 19:58:45.088+03	14	2	12298	\N
36902	+254700000000	Facility Manager	t	t	2025-09-01 19:58:46.383+03	2025-09-01 19:58:46.383+03	1	2	12299	\N
36903	info@holyfamilyhospitalna.com	Information Desk	f	t	2025-09-01 19:58:46.391+03	2025-09-01 19:58:46.391+03	2	2	12299	\N
36904	P.O BOX 57-50406 FUNYULA FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 100 BUSIA LICENCED		f	t	2025-09-01 19:58:46.398+03	2025-09-01 19:58:46.398+03	14	2	12299	\N
36905	+254700000000	Facility Manager	t	t	2025-09-01 19:58:46.472+03	2025-09-01 19:58:46.472+03	1	2	12300	\N
36906	info@cornerstonebaptist.com	Information Desk	f	t	2025-09-01 19:58:46.479+03	2025-09-01 19:58:46.479+03	2	2	12300	\N
36907	P.O BOX 2171-00200 NAIROBI FAITH BASED DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:46.487+03	2025-09-01 19:58:46.487+03	14	2	12300	\N
36908	+254700000000	Facility Manager	t	t	2025-09-01 19:58:47.842+03	2025-09-01 19:58:47.842+03	1	2	12301	\N
36909	info@tanakanursinghomebus.com	Information Desk	f	t	2025-09-01 19:58:47.85+03	2025-09-01 19:58:47.85+03	2	2	12301	\N
36910	P.O BOX 485-50400 BUSIA HOSPITAL LEVEL 4 Private LEVEL 4 110 BUSIA LICENCED		f	t	2025-09-01 19:58:47.858+03	2025-09-01 19:58:47.858+03	14	2	12301	\N
36911	+254700000000	Facility Manager	t	t	2025-09-01 19:58:49.241+03	2025-09-01 19:58:49.241+03	1	2	12302	\N
36912	info@newbusiamaternitynur.com	Information Desk	f	t	2025-09-01 19:58:49.252+03	2025-09-01 19:58:49.252+03	2	2	12302	\N
36913	P.O BOX 418-50400 BUSIA HOSPITAL LEVEL 4 Private LEVEL 4 60BUSIA LICENCED		f	t	2025-09-01 19:58:49.262+03	2025-09-01 19:58:49.262+03	14	2	12302	\N
36914	+254700000000	Facility Manager	t	t	2025-09-01 19:58:49.328+03	2025-09-01 19:58:49.328+03	1	2	12303	\N
36915	info@fahelmacfwcommunityc.com	Information Desk	f	t	2025-09-01 19:58:49.335+03	2025-09-01 19:58:49.335+03	2	2	12303	\N
36916	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:49.345+03	2025-09-01 19:58:49.345+03	14	2	12303	\N
36917	+254700000000	Facility Manager	t	t	2025-09-01 19:58:50.763+03	2025-09-01 19:58:50.763+03	1	2	12304	\N
36918	info@bumalacfwclinic.com	Information Desk	f	t	2025-09-01 19:58:50.77+03	2025-09-01 19:58:50.77+03	2	2	12304	\N
36919	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:50.777+03	2025-09-01 19:58:50.777+03	14	2	12304	\N
36920	+254700000000	Facility Manager	t	t	2025-09-01 19:58:50.848+03	2025-09-01 19:58:50.848+03	1	2	12305	\N
36921	info@namenyacfwclinic.com	Information Desk	f	t	2025-09-01 19:58:50.855+03	2025-09-01 19:58:50.856+03	2	2	12305	\N
36922	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:50.864+03	2025-09-01 19:58:50.864+03	14	2	12305	\N
36923	+254700000000	Facility Manager	t	t	2025-09-01 19:58:50.914+03	2025-09-01 19:58:50.914+03	1	2	12306	\N
36924	info@pesimedicalcentre.com	Information Desk	f	t	2025-09-01 19:58:50.921+03	2025-09-01 19:58:50.921+03	2	2	12306	\N
36925	P.O BOX 94-50400 BUSIA NURSING HOME Private LEVEL 3B 18BUSIA LICENCED		f	t	2025-09-01 19:58:50.928+03	2025-09-01 19:58:50.928+03	14	2	12306	\N
36926	+254700000000	Facility Manager	t	t	2025-09-01 19:58:50.98+03	2025-09-01 19:58:50.98+03	1	2	12307	\N
36927	info@theagakhanhospitalbu.com	Information Desk	f	t	2025-09-01 19:58:50.987+03	2025-09-01 19:58:50.987+03	2	2	12307	\N
36928	P.O BOX 530-40100 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED		f	t	2025-09-01 19:58:50.998+03	2025-09-01 19:58:50.998+03	14	2	12307	\N
36929	+254700000000	Facility Manager	t	t	2025-09-01 19:58:52.31+03	2025-09-01 19:58:52.31+03	1	2	12308	\N
36930	info@feithmedicalclinicbu.com	Information Desk	f	t	2025-09-01 19:58:52.319+03	2025-09-01 19:58:52.319+03	2	2	12308	\N
36931	P.O BOX 574- BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:52.327+03	2025-09-01 19:58:52.327+03	14	2	12308	\N
36932	+254700000000	Facility Manager	t	t	2025-09-01 19:58:53.803+03	2025-09-01 19:58:53.803+03	1	2	12309	\N
36933	info@busiaequatorclinic.com	Information Desk	f	t	2025-09-01 19:58:53.811+03	2025-09-01 19:58:53.811+03	2	2	12309	\N
36934	P.O BOX 87-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:53.819+03	2025-09-01 19:58:53.819+03	14	2	12309	\N
36935	+254700000000	Facility Manager	t	t	2025-09-01 19:58:55.623+03	2025-09-01 19:58:55.623+03	1	2	12310	\N
36936	info@busiabaseboarderfait.com	Information Desk	f	t	2025-09-01 19:58:55.631+03	2025-09-01 19:58:55.631+03	2	2	12310	\N
36937	P.O BOX 574-50400 BUSIA NURSING HOME Private LEVEL 3B 16BUSIA LICENCED		f	t	2025-09-01 19:58:55.639+03	2025-09-01 19:58:55.639+03	14	2	12310	\N
36938	+254700000000	Facility Manager	t	t	2025-09-01 19:58:57.773+03	2025-09-01 19:58:57.773+03	1	2	12311	\N
36939	info@stirlinghealthcareco.com	Information Desk	f	t	2025-09-01 19:58:57.781+03	2025-09-01 19:58:57.781+03	2	2	12311	\N
36940	P.O BOX 313-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:57.791+03	2025-09-01 19:58:57.791+03	14	2	12311	\N
36941	+254700000000	Facility Manager	t	t	2025-09-01 19:58:59.647+03	2025-09-01 19:58:59.647+03	1	2	12312	\N
36942	info@busiahealthsidelabme.com	Information Desk	f	t	2025-09-01 19:58:59.655+03	2025-09-01 19:58:59.655+03	2	2	12312	\N
36943	P.O BOX 155-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:58:59.662+03	2025-09-01 19:58:59.662+03	14	2	12312	\N
36944	+254700000000	Facility Manager	t	t	2025-09-01 19:59:01.58+03	2025-09-01 19:59:01.58+03	1	2	12313	\N
36945	info@bunyalamedicalclinic.com	Information Desk	f	t	2025-09-01 19:59:01.591+03	2025-09-01 19:59:01.591+03	2	2	12313	\N
36946	P.O BOX 940-50100 KAKAMEGA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:01.606+03	2025-09-01 19:59:01.606+03	14	2	12313	\N
36947	+254700000000	Facility Manager	t	t	2025-09-01 19:59:03.402+03	2025-09-01 19:59:03.402+03	1	2	12314	\N
36948	info@optexopticiansltdbus.com	Information Desk	f	t	2025-09-01 19:59:03.409+03	2025-09-01 19:59:03.409+03	2	2	12314	\N
36949	P.O BOX 11-50400 BUSIA EYE CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:03.422+03	2025-09-01 19:59:03.422+03	14	2	12314	\N
36950	+254700000000	Facility Manager	t	t	2025-09-01 19:59:04.818+03	2025-09-01 19:59:04.818+03	1	2	12315	\N
36951	info@visiongateeyecarecon.com	Information Desk	f	t	2025-09-01 19:59:04.827+03	2025-09-01 19:59:04.827+03	2	2	12315	\N
36952	P.O BOX 313-50400 BUSIA EYE CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:04.837+03	2025-09-01 19:59:04.837+03	14	2	12315	\N
36953	+254700000000	Facility Manager	t	t	2025-09-01 19:59:06.386+03	2025-09-01 19:59:06.386+03	1	2	12316	\N
36954	info@zurricottagehealthca.com	Information Desk	f	t	2025-09-01 19:59:06.395+03	2025-09-01 19:59:06.395+03	2	2	12316	\N
36955	P.O BOX 514-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:06.405+03	2025-09-01 19:59:06.405+03	14	2	12316	\N
36956	+254700000000	Facility Manager	t	t	2025-09-01 19:59:07.806+03	2025-09-01 19:59:07.806+03	1	2	12317	\N
36957	info@minallahimedicare.com	Information Desk	f	t	2025-09-01 19:59:07.82+03	2025-09-01 19:59:07.82+03	2	2	12317	\N
36958	P.O BOX -50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:07.828+03	2025-09-01 19:59:07.828+03	14	2	12317	\N
36959	+254700000000	Facility Manager	t	t	2025-09-01 19:59:09.619+03	2025-09-01 19:59:09.619+03	1	2	12318	\N
36960	info@blisshealthcareltdbu.com	Information Desk	f	t	2025-09-01 19:59:09.628+03	2025-09-01 19:59:09.628+03	2	2	12318	\N
36961	P.O BOX 5763-00200 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED		f	t	2025-09-01 19:59:09.636+03	2025-09-01 19:59:09.636+03	14	2	12318	\N
36962	+254700000000	Facility Manager	t	t	2025-09-01 19:59:11.017+03	2025-09-01 19:59:11.017+03	1	2	12319	\N
36963	info@amanecottagehospital.com	Information Desk	f	t	2025-09-01 19:59:11.023+03	2025-09-01 19:59:11.023+03	2	2	12319	\N
36964	P.O BOX 5532-30100 ELDORET COTTAGE HOSPITAL Private LEVEL 3B 13BUSIA LICENCED		f	t	2025-09-01 19:59:11.03+03	2025-09-01 19:59:11.03+03	14	2	12319	\N
36965	+254700000000	Facility Manager	t	t	2025-09-01 19:59:12.332+03	2025-09-01 19:59:12.332+03	1	2	12320	\N
36966	info@lumolamedicalclinic.com	Information Desk	f	t	2025-09-01 19:59:12.339+03	2025-09-01 19:59:12.339+03	2	2	12320	\N
36967	P.O BOX 35-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED		f	t	2025-09-01 19:59:12.347+03	2025-09-01 19:59:12.347+03	14	2	12320	\N
36968	+254700000000	Facility Manager	t	t	2025-09-01 19:59:13.631+03	2025-09-01 19:59:13.631+03	1	2	12321	\N
36969	info@nassihospitals.com	Information Desk	f	t	2025-09-01 19:59:13.637+03	2025-09-01 19:59:13.637+03	2	2	12321	\N
36970	P.O BOX 486-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 30BUSIA LICENCED		f	t	2025-09-01 19:59:13.645+03	2025-09-01 19:59:13.645+03	14	2	12321	\N
36971	+254700000000	Facility Manager	t	t	2025-09-01 19:59:15.216+03	2025-09-01 19:59:15.216+03	1	2	12322	\N
36972	info@medsparmedicalcentre.com	Information Desk	f	t	2025-09-01 19:59:15.223+03	2025-09-01 19:59:15.223+03	2	2	12322	\N
36973	P.O BOX 43-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:15.234+03	2025-09-01 19:59:15.234+03	14	2	12322	\N
36974	+254700000000	Facility Manager	t	t	2025-09-01 19:59:16.453+03	2025-09-01 19:59:16.453+03	1	2	12323	\N
36975	info@turningpointmedicalc.com	Information Desk	f	t	2025-09-01 19:59:16.461+03	2025-09-01 19:59:16.461+03	2	2	12323	\N
36976	P.O BOX 3-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED		f	t	2025-09-01 19:59:16.471+03	2025-09-01 19:59:16.471+03	14	2	12323	\N
36977	+254700000000	Facility Manager	t	t	2025-09-01 19:59:17.961+03	2025-09-01 19:59:17.961+03	1	2	12324	\N
36978	info@busiamedicalspeciali.com	Information Desk	f	t	2025-09-01 19:59:17.97+03	2025-09-01 19:59:17.97+03	2	2	12324	\N
36979	P.O BOX 2310-50200 BUSIA MEDICAL CENTRE Private LEVEL 3A 8BUSIA LICENCED		f	t	2025-09-01 19:59:17.977+03	2025-09-01 19:59:17.977+03	14	2	12324	\N
36980	+254700000000	Facility Manager	t	t	2025-09-01 19:59:19.628+03	2025-09-01 19:59:19.628+03	1	2	12325	\N
36981	info@brilliancecaremedica.com	Information Desk	f	t	2025-09-01 19:59:19.642+03	2025-09-01 19:59:19.642+03	2	2	12325	\N
36982	P.O BOX 856-40600 SIAYA MEDICAL CENTRE Private LEVEL 3A 15BUSIA LICENCED		f	t	2025-09-01 19:59:19.65+03	2025-09-01 19:59:19.65+03	14	2	12325	\N
36983	+254700000000	Facility Manager	t	t	2025-09-01 19:59:21.185+03	2025-09-01 19:59:21.185+03	1	2	12326	\N
36984	info@gangacfwclinic.com	Information Desk	f	t	2025-09-01 19:59:21.192+03	2025-09-01 19:59:21.193+03	2	2	12326	\N
36985	P.O BOX 1630-00600 NAIROBI MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:21.2+03	2025-09-01 19:59:21.2+03	14	2	12326	\N
36986	+254700000000	Facility Manager	t	t	2025-09-01 19:59:22.44+03	2025-09-01 19:59:22.44+03	1	2	12327	\N
36987	info@lebenmedicalserviceb.com	Information Desk	f	t	2025-09-01 19:59:22.447+03	2025-09-01 19:59:22.447+03	2	2	12327	\N
36988	P.O BOX 898-50100 KAKAMEGA NURSING HOME Private LEVEL 3B 40BUSIA LICENCED		f	t	2025-09-01 19:59:22.455+03	2025-09-01 19:59:22.455+03	14	2	12327	\N
36989	+254700000000	Facility Manager	t	t	2025-09-01 19:59:23.938+03	2025-09-01 19:59:23.939+03	1	2	12328	\N
36990	info@tomapsmedicalclinic.com	Information Desk	f	t	2025-09-01 19:59:23.946+03	2025-09-01 19:59:23.946+03	2	2	12328	\N
36991	P.O BOX 190-50100 KAKAMEGA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:23.954+03	2025-09-01 19:59:23.954+03	14	2	12328	\N
36992	+254700000000	Facility Manager	t	t	2025-09-01 19:59:25.224+03	2025-09-01 19:59:25.224+03	1	2	12329	\N
36993	info@brimaxahospitallimit.com	Information Desk	f	t	2025-09-01 19:59:25.233+03	2025-09-01 19:59:25.233+03	2	2	12329	\N
36994	P.O BOX 38133-00100 NAIROBI HOSPITAL LEVEL 4 Private LEVEL 4 60BUSIA LICENCED		f	t	2025-09-01 19:59:25.24+03	2025-09-01 19:59:25.24+03	14	2	12329	\N
36995	+254700000000	Facility Manager	t	t	2025-09-01 19:59:26.516+03	2025-09-01 19:59:26.516+03	1	2	12330	\N
36996	info@goodhopehealthlimite.com	Information Desk	f	t	2025-09-01 19:59:26.524+03	2025-09-01 19:59:26.524+03	2	2	12330	\N
36997	P.O BOX 10548-30100 BUSIA HOSPITAL LEVEL 4 Private LEVEL 4 42BUSIA LICENCED		f	t	2025-09-01 19:59:26.535+03	2025-09-01 19:59:26.535+03	14	2	12330	\N
36998	+254700000000	Facility Manager	t	t	2025-09-01 19:59:28.293+03	2025-09-01 19:59:28.293+03	1	2	12331	\N
36999	info@raimuhospitallimited.com	Information Desk	f	t	2025-09-01 19:59:28.301+03	2025-09-01 19:59:28.301+03	2	2	12331	\N
37000	P.O BOX 2448-50200 BUNGOMA MEDICAL CENTRE Private LEVEL 3A 25BUSIA LICENCED		f	t	2025-09-01 19:59:28.308+03	2025-09-01 19:59:28.308+03	14	2	12331	\N
37001	+254700000000	Facility Manager	t	t	2025-09-01 19:59:29.613+03	2025-09-01 19:59:29.613+03	1	2	12332	\N
37002	info@st.jamesinfirmarybus.com	Information Desk	f	t	2025-09-01 19:59:29.635+03	2025-09-01 19:59:29.635+03	2	2	12332	\N
37003	P.O BOX 1108-50400 BUSIA NURSING HOME Private LEVEL 3B 30BUSIA LICENCED		f	t	2025-09-01 19:59:29.648+03	2025-09-01 19:59:29.649+03	14	2	12332	\N
37004	+254700000000	Facility Manager	t	t	2025-09-01 19:59:31.275+03	2025-09-01 19:59:31.275+03	1	2	12333	\N
37005	info@oasisdoctorsplazabus.com	Information Desk	f	t	2025-09-01 19:59:31.292+03	2025-09-01 19:59:31.292+03	2	2	12333	\N
37006	P.O BOX 201-50400 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED		f	t	2025-09-01 19:59:31.308+03	2025-09-01 19:59:31.308+03	14	2	12333	\N
37007	+254700000000	Facility Manager	t	t	2025-09-01 19:59:32.97+03	2025-09-01 19:59:32.97+03	1	2	12334	\N
37008	info@blossomdentalclinicl.com	Information Desk	f	t	2025-09-01 19:59:32.978+03	2025-09-01 19:59:32.978+03	2	2	12334	\N
37009	P.O BOX 2415-40100 KISUMU DENTAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:32.986+03	2025-09-01 19:59:32.986+03	14	2	12334	\N
37010	+254700000000	Facility Manager	t	t	2025-09-01 19:59:34.353+03	2025-09-01 19:59:34.353+03	1	2	12335	\N
37011	info@esikomacommunityhosp.com	Information Desk	f	t	2025-09-01 19:59:34.36+03	2025-09-01 19:59:34.36+03	2	2	12335	\N
37012	P.O BOX 2395-50100 KAKAMEGA MEDICAL CENTRE Private LEVEL 3A 18BUSIA LICENCED		f	t	2025-09-01 19:59:34.369+03	2025-09-01 19:59:34.369+03	14	2	12335	\N
37013	+254700000000	Facility Manager	t	t	2025-09-01 19:59:35.698+03	2025-09-01 19:59:35.698+03	1	2	12336	\N
37014	info@alinacarehealthservi.com	Information Desk	f	t	2025-09-01 19:59:35.705+03	2025-09-01 19:59:35.705+03	2	2	12336	\N
37015	P.O BOX 302-50400 BUSIA MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:35.712+03	2025-09-01 19:59:35.712+03	14	2	12336	\N
37016	+254700000000	Facility Manager	t	t	2025-09-01 19:59:37.019+03	2025-09-01 19:59:37.019+03	1	2	12337	\N
37017	info@chalondrahealthcarec.com	Information Desk	f	t	2025-09-01 19:59:37.028+03	2025-09-01 19:59:37.028+03	2	2	12337	\N
37018	P.O BOX 3232-40100 KISUMU MEDICAL CLINIC Private LEVEL 2 0BUSIA LICENCED		f	t	2025-09-01 19:59:37.036+03	2025-09-01 19:59:37.036+03	14	2	12337	\N
37019	+254700000000	Facility Manager	t	t	2025-09-01 19:59:38.605+03	2025-09-01 19:59:38.605+03	1	2	12338	\N
37020	info@bulwaniprivatehospit.com	Information Desk	f	t	2025-09-01 19:59:38.612+03	2025-09-01 19:59:38.612+03	2	2	12338	\N
37021	P.O BOX 64-50405 BUSIA MEDICAL CENTRE Private LEVEL 3A 0BUSIA LICENCED		f	t	2025-09-01 19:59:38.62+03	2025-09-01 19:59:38.62+03	14	2	12338	\N
37022	+254700000000	Facility Manager	t	t	2025-09-01 19:59:40.095+03	2025-09-01 19:59:40.095+03	1	2	12339	\N
37023	info@endohealthcentremiss.com	Information Desk	f	t	2025-09-01 19:59:40.103+03	2025-09-01 19:59:40.103+03	2	2	12339	\N
37024	P.O BOX 8409-30100 ELDORET HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 24ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:40.111+03	2025-09-01 19:59:40.111+03	14	2	12339	\N
37025	+254700000000	Facility Manager	t	t	2025-09-01 19:59:41.379+03	2025-09-01 19:59:41.379+03	1	2	12340	\N
37026	info@embobutcatholicmissi.com	Information Desk	f	t	2025-09-01 19:59:41.389+03	2025-09-01 19:59:41.389+03	2	2	12340	\N
37027	P.O BOX 256-30705 ELDORET DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:41.397+03	2025-09-01 19:59:41.397+03	14	2	12340	\N
37028	+254700000000	Facility Manager	t	t	2025-09-01 19:59:42.855+03	2025-09-01 19:59:42.855+03	1	2	12341	\N
37029	info@kapkoihealthcentre.com	Information Desk	f	t	2025-09-01 19:59:42.862+03	2025-09-01 19:59:42.862+03	2	2	12341	\N
37030	P.O BOX 1890-30100 ELDORET HEALTH CENTRE Private LEVEL 3B 10ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:42.868+03	2025-09-01 19:59:42.868+03	14	2	12341	\N
37031	+254700000000	Facility Manager	t	t	2025-09-01 19:59:42.961+03	2025-09-01 19:59:42.961+03	1	2	12342	\N
37032	info@chesongochmissionhos.com	Information Desk	f	t	2025-09-01 19:59:42.968+03	2025-09-01 19:59:42.968+03	2	2	12342	\N
37033	P.O BOX 8409-30100 ELDORET FAITH BASED LEVEL 4 HOSPITAL Private LEVEL 4 56ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:42.978+03	2025-09-01 19:59:42.978+03	14	2	12342	\N
37034	+254700000000	Facility Manager	t	t	2025-09-01 19:59:44.456+03	2025-09-01 19:59:44.456+03	1	2	12343	\N
37035	info@blisshealthcareltdit.com	Information Desk	f	t	2025-09-01 19:59:44.464+03	2025-09-01 19:59:44.464+03	2	2	12343	\N
37036	P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:44.471+03	2025-09-01 19:59:44.471+03	14	2	12343	\N
37037	+254700000000	Facility Manager	t	t	2025-09-01 19:59:45.83+03	2025-09-01 19:59:45.83+03	1	2	12344	\N
37038	info@cheptongeimedicalcli.com	Information Desk	f	t	2025-09-01 19:59:45.848+03	2025-09-01 19:59:45.848+03	2	2	12344	\N
37039	P.O BOX 3790-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:45.855+03	2025-09-01 19:59:45.855+03	14	2	12344	\N
37040	+254700000000	Facility Manager	t	t	2025-09-01 19:59:47.156+03	2025-09-01 19:59:47.156+03	1	2	12345	\N
37041	info@ljmalelmedicalcentre.com	Information Desk	f	t	2025-09-01 19:59:47.166+03	2025-09-01 19:59:47.166+03	2	2	12345	\N
37042	P.O BOX 10583-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:47.175+03	2025-09-01 19:59:47.175+03	14	2	12345	\N
37043	+254700000000	Facility Manager	t	t	2025-09-01 19:59:48.283+03	2025-09-01 19:59:48.283+03	1	2	12346	\N
37044	info@flaxsavanismedicalce.com	Information Desk	f	t	2025-09-01 19:59:48.291+03	2025-09-01 19:59:48.291+03	2	2	12346	\N
37045	P.O BOX 2594-30100 ELDORET MEDICAL CLINIC Private LEVEL 2 0ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:48.302+03	2025-09-01 19:59:48.302+03	14	2	12346	\N
37046	+254700000000	Facility Manager	t	t	2025-09-01 19:59:49.758+03	2025-09-01 19:59:49.758+03	1	2	12347	\N
37047	info@invelahealthcareltd.com	Information Desk	f	t	2025-09-01 19:59:49.768+03	2025-09-01 19:59:49.768+03	2	2	12347	\N
37048	P.O BOX 692-30100 ELDORET MEDICAL CENTRE Private LEVEL 3A 8ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:49.785+03	2025-09-01 19:59:49.785+03	14	2	12347	\N
37049	+254700000000	Facility Manager	t	t	2025-09-01 19:59:51.376+03	2025-09-01 19:59:51.376+03	1	2	12348	\N
37050	info@equityafialimitedite.com	Information Desk	f	t	2025-09-01 19:59:51.385+03	2025-09-01 19:59:51.385+03	2	2	12348	\N
37051	P.O BOX 75104-00200 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0ELGEYO MARAKWET LICENCED		f	t	2025-09-01 19:59:51.392+03	2025-09-01 19:59:51.392+03	14	2	12348	\N
37052	+254700000000	Facility Manager	t	t	2025-09-01 19:59:52.819+03	2025-09-01 19:59:52.819+03	1	2	12349	\N
37053	info@st.augustinecfwclini.com	Information Desk	f	t	2025-09-01 19:59:52.826+03	2025-09-01 19:59:52.826+03	2	2	12349	\N
37054	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 19:59:52.84+03	2025-09-01 19:59:52.84+03	14	2	12349	\N
37055	+254700000000	Facility Manager	t	t	2025-09-01 19:59:54.227+03	2025-09-01 19:59:54.227+03	1	2	12350	\N
37056	info@st.anthonycfwclinic.com	Information Desk	f	t	2025-09-01 19:59:54.245+03	2025-09-01 19:59:54.245+03	2	2	12350	\N
37057	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 19:59:54.253+03	2025-09-01 19:59:54.253+03	14	2	12350	\N
37058	+254700000000	Facility Manager	t	t	2025-09-01 19:59:55.754+03	2025-09-01 19:59:55.754+03	1	2	12351	\N
37059	info@st.nicholasc.f.wclin.com	Information Desk	f	t	2025-09-01 19:59:55.761+03	2025-09-01 19:59:55.761+03	2	2	12351	\N
37060	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 19:59:55.771+03	2025-09-01 19:59:55.771+03	14	2	12351	\N
37061	+254700000000	Facility Manager	t	t	2025-09-01 19:59:56.986+03	2025-09-01 19:59:56.986+03	1	2	12352	\N
37062	info@tenderlovingcarecfwc.com	Information Desk	f	t	2025-09-01 19:59:56.995+03	2025-09-01 19:59:56.995+03	2	2	12352	\N
37063	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 19:59:57.003+03	2025-09-01 19:59:57.003+03	14	2	12352	\N
37064	+254700000000	Facility Manager	t	t	2025-09-01 19:59:57.089+03	2025-09-01 19:59:57.089+03	1	2	12353	\N
37065	info@embucountyreferralho.com	Information Desk	f	t	2025-09-01 19:59:57.096+03	2025-09-01 19:59:57.096+03	2	2	12353	\N
37066	P.O BOX 33-60100 EMBU Hospital Level 5 Public LEVEL 5 618 EMBU LICENCED		f	t	2025-09-01 19:59:57.105+03	2025-09-01 19:59:57.105+03	14	2	12353	\N
37067	+254700000000	Facility Manager	t	t	2025-09-01 19:59:58.441+03	2025-09-01 19:59:58.441+03	1	2	12354	\N
37068	info@universityofembudepa.com	Information Desk	f	t	2025-09-01 19:59:58.448+03	2025-09-01 19:59:58.448+03	2	2	12354	\N
37069	P.O BOX 6-60100 EMBU DISPENSARY Public LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 19:59:58.456+03	2025-09-01 19:59:58.456+03	14	2	12354	\N
37070	+254700000000	Facility Manager	t	t	2025-09-01 20:00:00.202+03	2025-09-01 20:00:00.202+03	1	2	12355	\N
37071	info@consolatahospitalkye.com	Information Desk	f	t	2025-09-01 20:00:00.209+03	2025-09-01 20:00:00.209+03	2	2	12355	\N
37072	P.O BOX 38-60103 RUNYENJES FAITH BASED LEVEL 5 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 5 280 EMBU LICENCED		f	t	2025-09-01 20:00:00.215+03	2025-09-01 20:00:00.215+03	14	2	12355	\N
37073	+254700000000	Facility Manager	t	t	2025-09-01 20:00:00.29+03	2025-09-01 20:00:00.29+03	1	2	12356	\N
37074	info@geltrudehealthcentre.com	Information Desk	f	t	2025-09-01 20:00:00.305+03	2025-09-01 20:00:00.305+03	2	2	12356	\N
37075	P.O BOX 2099-60100 EMBU HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 6EMBU LICENCED		f	t	2025-09-01 20:00:00.32+03	2025-09-01 20:00:00.32+03	14	2	12356	\N
37076	+254700000000	Facility Manager	t	t	2025-09-01 20:00:01.991+03	2025-09-01 20:00:01.991+03	1	2	12357	\N
37077	info@livierodispensary.com	Information Desk	f	t	2025-09-01 20:00:02.012+03	2025-09-01 20:00:02.012+03	2	2	12357	\N
37078	P.O BOX 2099-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:02.032+03	2025-09-01 20:00:02.032+03	14	2	12357	\N
37079	+254700000000	Facility Manager	t	t	2025-09-01 20:00:02.154+03	2025-09-01 20:00:02.154+03	1	2	12358	\N
37080	info@st.marysdispensaryng.com	Information Desk	f	t	2025-09-01 20:00:02.162+03	2025-09-01 20:00:02.162+03	2	2	12358	\N
37081	P.O BOX 194-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:02.169+03	2025-09-01 20:00:02.169+03	14	2	12358	\N
37082	+254700000000	Facility Manager	t	t	2025-09-01 20:00:02.258+03	2025-09-01 20:00:02.258+03	1	2	12359	\N
37083	info@ackkiriaridispensary.com	Information Desk	f	t	2025-09-01 20:00:02.279+03	2025-09-01 20:00:02.279+03	2	2	12359	\N
37084	P.O BOX 2467-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:02.298+03	2025-09-01 20:00:02.298+03	14	2	12359	\N
37085	+254700000000	Facility Manager	t	t	2025-09-01 20:00:03.463+03	2025-09-01 20:00:03.463+03	1	2	12360	\N
37086	info@mothermazzarellodisp.com	Information Desk	f	t	2025-09-01 20:00:03.473+03	2025-09-01 20:00:03.473+03	2	2	12360	\N
37087	P.O BOX 1154-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:03.48+03	2025-09-01 20:00:03.48+03	14	2	12360	\N
37088	+254700000000	Facility Manager	t	t	2025-09-01 20:00:04.768+03	2025-09-01 20:00:04.768+03	1	2	12361	\N
37089	info@kevotecatholicdispen.com	Information Desk	f	t	2025-09-01 20:00:04.776+03	2025-09-01 20:00:04.776+03	2	2	12361	\N
37090	P.O BOX 24-60100 EMBU DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:04.783+03	2025-09-01 20:00:04.783+03	14	2	12361	\N
37091	+254700000000	Facility Manager	t	t	2025-09-01 20:00:04.847+03	2025-09-01 20:00:04.847+03	1	2	12362	\N
37092	info@joykimnursinghome.com	Information Desk	f	t	2025-09-01 20:00:04.855+03	2025-09-01 20:00:04.855+03	2	2	12362	\N
37093	P.O BOX 986-60100 EMBU NURSING HOME Private LEVEL 3B 30EMBU LICENCED		f	t	2025-09-01 20:00:04.863+03	2025-09-01 20:00:04.863+03	14	2	12362	\N
37094	+254700000000	Facility Manager	t	t	2025-09-01 20:00:04.928+03	2025-09-01 20:00:04.928+03	1	2	12363	\N
37095	info@libertymaternityandn.com	Information Desk	f	t	2025-09-01 20:00:04.935+03	2025-09-01 20:00:04.935+03	2	2	12363	\N
37096	P.O BOX 2143-60100 EMBU NURSING HOME Private LEVEL 3B 26EMBU LICENCED		f	t	2025-09-01 20:00:04.944+03	2025-09-01 20:00:04.944+03	14	2	12363	\N
37097	+254700000000	Facility Manager	t	t	2025-09-01 20:00:05.007+03	2025-09-01 20:00:05.007+03	1	2	12364	\N
37098	info@st.teresacfwclinic.com	Information Desk	f	t	2025-09-01 20:00:05.023+03	2025-09-01 20:00:05.023+03	2	2	12364	\N
37099	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:05.032+03	2025-09-01 20:00:05.032+03	14	2	12364	\N
37100	+254700000000	Facility Manager	t	t	2025-09-01 20:00:06.241+03	2025-09-01 20:00:06.241+03	1	2	12365	\N
37101	info@faithcfwclinic.com	Information Desk	f	t	2025-09-01 20:00:06.25+03	2025-09-01 20:00:06.25+03	2	2	12365	\N
37102	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:06.259+03	2025-09-01 20:00:06.259+03	14	2	12365	\N
37103	+254700000000	Facility Manager	t	t	2025-09-01 20:00:07.895+03	2025-09-01 20:00:07.895+03	1	2	12366	\N
37104	info@afyalinecfwclinic.com	Information Desk	f	t	2025-09-01 20:00:07.902+03	2025-09-01 20:00:07.902+03	2	2	12366	\N
37105	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:07.91+03	2025-09-01 20:00:07.91+03	14	2	12366	\N
37106	+254700000000	Facility Manager	t	t	2025-09-01 20:00:09.17+03	2025-09-01 20:00:09.17+03	1	2	12367	\N
37107	info@joycfwclinic.com	Information Desk	f	t	2025-09-01 20:00:09.178+03	2025-09-01 20:00:09.178+03	2	2	12367	\N
37108	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:09.19+03	2025-09-01 20:00:09.19+03	14	2	12367	\N
37109	+254700000000	Facility Manager	t	t	2025-09-01 20:00:10.482+03	2025-09-01 20:00:10.482+03	1	2	12368	\N
37110	info@patiencecfwclinic.com	Information Desk	f	t	2025-09-01 20:00:10.49+03	2025-09-01 20:00:10.49+03	2	2	12368	\N
37111	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:10.498+03	2025-09-01 20:00:10.498+03	14	2	12368	\N
37112	+254700000000	Facility Manager	t	t	2025-09-01 20:00:11.899+03	2025-09-01 20:00:11.9+03	1	2	12369	\N
37113	info@mweadentalclinic.com	Information Desk	f	t	2025-09-01 20:00:11.907+03	2025-09-01 20:00:11.907+03	2	2	12369	\N
37114	P.O BOX 1698- EMBU DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:11.916+03	2025-09-01 20:00:11.916+03	14	2	12369	\N
37115	+254700000000	Facility Manager	t	t	2025-09-01 20:00:11.989+03	2025-09-01 20:00:11.989+03	1	2	12370	\N
37116	info@countymedicalcentree.com	Information Desk	f	t	2025-09-01 20:00:11.996+03	2025-09-01 20:00:11.996+03	2	2	12370	\N
37117	P.O BOX 558-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 52EMBU LICENCED		f	t	2025-09-01 20:00:12.005+03	2025-09-01 20:00:12.005+03	14	2	12370	\N
37118	+254700000000	Facility Manager	t	t	2025-09-01 20:00:12.073+03	2025-09-01 20:00:12.073+03	1	2	12371	\N
37119	info@embuchildrensclinic.com	Information Desk	f	t	2025-09-01 20:00:12.081+03	2025-09-01 20:00:12.081+03	2	2	12371	\N
37120	P.O BOX 1698-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 35EMBU LICENCED		f	t	2025-09-01 20:00:12.09+03	2025-09-01 20:00:12.09+03	14	2	12371	\N
37121	+254700000000	Facility Manager	t	t	2025-09-01 20:00:13.511+03	2025-09-01 20:00:13.511+03	1	2	12372	\N
37122	info@jetmaclinic.com	Information Desk	f	t	2025-09-01 20:00:13.523+03	2025-09-01 20:00:13.523+03	2	2	12372	\N
37123	P.O BOX 1569- EMBU MEDICAL CLINIC Private LEVEL 2 2EMBU LICENCED		f	t	2025-09-01 20:00:13.533+03	2025-09-01 20:00:13.534+03	14	2	12372	\N
37124	+254700000000	Facility Manager	t	t	2025-09-01 20:00:13.627+03	2025-09-01 20:00:13.627+03	1	2	12373	\N
37125	info@promisecfwclinic.com	Information Desk	f	t	2025-09-01 20:00:13.638+03	2025-09-01 20:00:13.638+03	2	2	12373	\N
37126	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:13.648+03	2025-09-01 20:00:13.649+03	14	2	12373	\N
37127	+254700000000	Facility Manager	t	t	2025-09-01 20:00:14.83+03	2025-09-01 20:00:14.83+03	1	2	12374	\N
37128	info@cfwmbuvoreclinic.com	Information Desk	f	t	2025-09-01 20:00:14.84+03	2025-09-01 20:00:14.84+03	2	2	12374	\N
37129	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:14.847+03	2025-09-01 20:00:14.847+03	14	2	12374	\N
37130	+254700000000	Facility Manager	t	t	2025-09-01 20:00:16.04+03	2025-09-01 20:00:16.04+03	1	2	12375	\N
37131	info@kimangarucfwclinic.com	Information Desk	f	t	2025-09-01 20:00:16.049+03	2025-09-01 20:00:16.049+03	2	2	12375	\N
37132	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:16.057+03	2025-09-01 20:00:16.057+03	14	2	12375	\N
37133	+254700000000	Facility Manager	t	t	2025-09-01 20:00:17.296+03	2025-09-01 20:00:17.296+03	1	2	12376	\N
37134	info@theagakhanuniversity.com	Information Desk	f	t	2025-09-01 20:00:17.303+03	2025-09-01 20:00:17.303+03	2	2	12376	\N
37135	P.O BOX 30270-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED		f	t	2025-09-01 20:00:17.31+03	2025-09-01 20:00:17.31+03	14	2	12376	\N
37136	+254700000000	Facility Manager	t	t	2025-09-01 20:00:17.396+03	2025-09-01 20:00:17.396+03	1	2	12377	\N
37137	info@kavutiricfwclinic.com	Information Desk	f	t	2025-09-01 20:00:17.404+03	2025-09-01 20:00:17.404+03	2	2	12377	\N
37138	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:17.41+03	2025-09-01 20:00:17.41+03	14	2	12377	\N
37139	+254700000000	Facility Manager	t	t	2025-09-01 20:00:18.792+03	2025-09-01 20:00:18.792+03	1	2	12378	\N
37140	info@hurumacfwclinic.com	Information Desk	f	t	2025-09-01 20:00:18.799+03	2025-09-01 20:00:18.799+03	2	2	12378	\N
37141	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:18.808+03	2025-09-01 20:00:18.808+03	14	2	12378	\N
37142	+254700000000	Facility Manager	t	t	2025-09-01 20:00:19.947+03	2025-09-01 20:00:19.947+03	1	2	12379	\N
37143	info@focusclinicalanddiag.com	Information Desk	f	t	2025-09-01 20:00:19.953+03	2025-09-01 20:00:19.953+03	2	2	12379	\N
37144	P.O BOX 783-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED		f	t	2025-09-01 20:00:19.96+03	2025-09-01 20:00:19.96+03	14	2	12379	\N
37145	+254700000000	Facility Manager	t	t	2025-09-01 20:00:21.539+03	2025-09-01 20:00:21.539+03	1	2	12380	\N
37146	info@utugicfwclinic.com	Information Desk	f	t	2025-09-01 20:00:21.548+03	2025-09-01 20:00:21.548+03	2	2	12380	\N
37147	P.O BOX 1630-00606 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:21.557+03	2025-09-01 20:00:21.557+03	14	2	12380	\N
37148	+254700000000	Facility Manager	t	t	2025-09-01 20:00:22.991+03	2025-09-01 20:00:22.991+03	1	2	12381	\N
37149	info@kingscaremedicallimi.com	Information Desk	f	t	2025-09-01 20:00:22.999+03	2025-09-01 20:00:22.999+03	2	2	12381	\N
37150	P.O BOX 1002-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 19EMBU LICENCED		f	t	2025-09-01 20:00:23.008+03	2025-09-01 20:00:23.008+03	14	2	12381	\N
37151	+254700000000	Facility Manager	t	t	2025-09-01 20:00:24.397+03	2025-09-01 20:00:24.397+03	1	2	12382	\N
37152	info@yunasimedicalcentre.com	Information Desk	f	t	2025-09-01 20:00:24.411+03	2025-09-01 20:00:24.411+03	2	2	12382	\N
37153	P.O BOX 2930-60200 MERU MEDICAL CENTRE Private LEVEL 3A 20EMBU LICENCED		f	t	2025-09-01 20:00:24.418+03	2025-09-01 20:00:24.418+03	14	2	12382	\N
37154	+254700000000	Facility Manager	t	t	2025-09-01 20:00:25.69+03	2025-09-01 20:00:25.69+03	1	2	12383	\N
37155	info@outspanhospitalembum.com	Information Desk	f	t	2025-09-01 20:00:25.698+03	2025-09-01 20:00:25.698+03	2	2	12383	\N
37156	P.O BOX 2490-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:25.712+03	2025-09-01 20:00:25.712+03	14	2	12383	\N
37157	+254700000000	Facility Manager	t	t	2025-09-01 20:00:27.098+03	2025-09-01 20:00:27.098+03	1	2	12384	\N
37158	info@eastenddentalclinicl.com	Information Desk	f	t	2025-09-01 20:00:27.112+03	2025-09-01 20:00:27.112+03	2	2	12384	\N
37159	P.O BOX 48580-00100 NAIROBI DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:27.12+03	2025-09-01 20:00:27.12+03	14	2	12384	\N
37160	+254700000000	Facility Manager	t	t	2025-09-01 20:00:27.271+03	2025-09-01 20:00:27.271+03	1	2	12385	\N
37161	info@pottersfamilyhospita.com	Information Desk	f	t	2025-09-01 20:00:27.28+03	2025-09-01 20:00:27.28+03	2	2	12385	\N
37162	P.O BOX 1822-60100 EMBU NURSING HOME Private LEVEL 3B 50EMBU LICENCED		f	t	2025-09-01 20:00:27.286+03	2025-09-01 20:00:27.286+03	14	2	12385	\N
37163	+254700000000	Facility Manager	t	t	2025-09-01 20:00:28.532+03	2025-09-01 20:00:28.532+03	1	2	12386	\N
37164	info@greenspanmedicalcent.com	Information Desk	f	t	2025-09-01 20:00:28.539+03	2025-09-01 20:00:28.539+03	2	2	12386	\N
37165	P.O BOX 534-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 15EMBU LICENCED		f	t	2025-09-01 20:00:28.547+03	2025-09-01 20:00:28.547+03	14	2	12386	\N
37166	+254700000000	Facility Manager	t	t	2025-09-01 20:00:29.805+03	2025-09-01 20:00:29.805+03	1	2	12387	\N
37167	info@optidentdentalcare.com	Information Desk	f	t	2025-09-01 20:00:29.82+03	2025-09-01 20:00:29.82+03	2	2	12387	\N
37168	P.O BOX 103597-00101 NAIROBI DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:29.833+03	2025-09-01 20:00:29.833+03	14	2	12387	\N
37169	+254700000000	Facility Manager	t	t	2025-09-01 20:00:30.96+03	2025-09-01 20:00:30.96+03	1	2	12388	\N
37170	info@makutanofamilyhealth.com	Information Desk	f	t	2025-09-01 20:00:30.967+03	2025-09-01 20:00:30.967+03	2	2	12388	\N
37171	P.O BOX 2477-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:30.973+03	2025-09-01 20:00:30.973+03	14	2	12388	\N
37172	+254700000000	Facility Manager	t	t	2025-09-01 20:00:32.442+03	2025-09-01 20:00:32.442+03	1	2	12389	\N
37173	info@kirimaraopticalsltde.com	Information Desk	f	t	2025-09-01 20:00:32.45+03	2025-09-01 20:00:32.45+03	2	2	12389	\N
37174	P.O BOX 2108-60100 EMBU EYE CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:32.456+03	2025-09-01 20:00:32.456+03	14	2	12389	\N
37175	+254700000000	Facility Manager	t	t	2025-09-01 20:00:33.814+03	2025-09-01 20:00:33.814+03	1	2	12390	\N
37176	info@daimamedicalclinicda.com	Information Desk	f	t	2025-09-01 20:00:33.832+03	2025-09-01 20:00:33.832+03	2	2	12390	\N
37177	P.O BOX 1905-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:33.853+03	2025-09-01 20:00:33.853+03	14	2	12390	\N
37178	+254700000000	Facility Manager	t	t	2025-09-01 20:00:35.448+03	2025-09-01 20:00:35.448+03	1	2	12391	\N
37179	info@odicaremedicalclinic.com	Information Desk	f	t	2025-09-01 20:00:35.455+03	2025-09-01 20:00:35.455+03	2	2	12391	\N
37180	P.O BOX 38- EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:35.462+03	2025-09-01 20:00:35.462+03	14	2	12391	\N
37181	+254700000000	Facility Manager	t	t	2025-09-01 20:00:36.983+03	2025-09-01 20:00:36.983+03	1	2	12392	\N
37182	info@angelcaremedicalclin.com	Information Desk	f	t	2025-09-01 20:00:36.991+03	2025-09-01 20:00:36.991+03	2	2	12392	\N
37183	P.O BOX 50- EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:36.998+03	2025-09-01 20:00:36.998+03	14	2	12392	\N
37184	+254700000000	Facility Manager	t	t	2025-09-01 20:00:38.191+03	2025-09-01 20:00:38.191+03	1	2	12393	\N
37185	info@embutumainimedicalse.com	Information Desk	f	t	2025-09-01 20:00:38.198+03	2025-09-01 20:00:38.198+03	2	2	12393	\N
37186	P.O BOX 2211-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:38.207+03	2025-09-01 20:00:38.207+03	14	2	12393	\N
37187	+254700000000	Facility Manager	t	t	2025-09-01 20:00:39.541+03	2025-09-01 20:00:39.541+03	1	2	12394	\N
37188	info@elimundanihealthcare.com	Information Desk	f	t	2025-09-01 20:00:39.547+03	2025-09-01 20:00:39.547+03	2	2	12394	\N
37189	P.O BOX 25493-00603 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:39.555+03	2025-09-01 20:00:39.555+03	14	2	12394	\N
37190	+254700000000	Facility Manager	t	t	2025-09-01 20:00:41.092+03	2025-09-01 20:00:41.092+03	1	2	12395	\N
37191	info@embuchildrenhospital.com	Information Desk	f	t	2025-09-01 20:00:41.099+03	2025-09-01 20:00:41.099+03	2	2	12395	\N
37192	P.O BOX 1698-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:41.107+03	2025-09-01 20:00:41.107+03	14	2	12395	\N
37193	+254700000000	Facility Manager	t	t	2025-09-01 20:00:42.592+03	2025-09-01 20:00:42.592+03	1	2	12396	\N
37194	info@smartsmiledentalcent.com	Information Desk	f	t	2025-09-01 20:00:42.601+03	2025-09-01 20:00:42.601+03	2	2	12396	\N
37195	P.O BOX 329-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED		f	t	2025-09-01 20:00:42.609+03	2025-09-01 20:00:42.609+03	14	2	12396	\N
37196	+254700000000	Facility Manager	t	t	2025-09-01 20:00:43.929+03	2025-09-01 20:00:43.929+03	1	2	12397	\N
37197	info@embumedicalanddental.com	Information Desk	f	t	2025-09-01 20:00:43.937+03	2025-09-01 20:00:43.937+03	2	2	12397	\N
37198	P.O BOX 1191-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:43.945+03	2025-09-01 20:00:43.945+03	14	2	12397	\N
37199	+254700000000	Facility Manager	t	t	2025-09-01 20:00:45.217+03	2025-09-01 20:00:45.217+03	1	2	12398	\N
37200	info@imarahospital.com	Information Desk	f	t	2025-09-01 20:00:45.225+03	2025-09-01 20:00:45.225+03	2	2	12398	\N
37201	P.O BOX 1446-60100 EMBU NURSING HOME Private LEVEL 3B 12EMBU LICENCED		f	t	2025-09-01 20:00:45.235+03	2025-09-01 20:00:45.235+03	14	2	12398	\N
37202	+254700000000	Facility Manager	t	t	2025-09-01 20:00:45.322+03	2025-09-01 20:00:45.322+03	1	2	12399	\N
37203	info@shanwesmedcare.com	Information Desk	f	t	2025-09-01 20:00:45.335+03	2025-09-01 20:00:45.335+03	2	2	12399	\N
37204	P.O BOX 2558-60200 MERU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:45.341+03	2025-09-01 20:00:45.341+03	14	2	12399	\N
37205	+254700000000	Facility Manager	t	t	2025-09-01 20:00:46.614+03	2025-09-01 20:00:46.614+03	1	2	12400	\N
37206	info@mtkenyaheartanddiabe.com	Information Desk	f	t	2025-09-01 20:00:46.636+03	2025-09-01 20:00:46.636+03	2	2	12400	\N
37207	P.O BOX 940-00618 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:46.651+03	2025-09-01 20:00:46.651+03	14	2	12400	\N
37208	+254700000000	Facility Manager	t	t	2025-09-01 20:00:48.537+03	2025-09-01 20:00:48.537+03	1	2	12401	\N
37209	info@visionnersmedicalcen.com	Information Desk	f	t	2025-09-01 20:00:48.545+03	2025-09-01 20:00:48.545+03	2	2	12401	\N
37210	P.O BOX 194-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 30EMBU LICENCED		f	t	2025-09-01 20:00:48.555+03	2025-09-01 20:00:48.555+03	14	2	12401	\N
37211	+254700000000	Facility Manager	t	t	2025-09-01 20:00:50.443+03	2025-09-01 20:00:50.443+03	1	2	12402	\N
37212	info@murithimethooptometr.com	Information Desk	f	t	2025-09-01 20:00:50.456+03	2025-09-01 20:00:50.456+03	2	2	12402	\N
37213	P.O BOX 2475-60100 EMBU EYE CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:50.464+03	2025-09-01 20:00:50.464+03	14	2	12402	\N
37214	+254700000000	Facility Manager	t	t	2025-09-01 20:00:52.098+03	2025-09-01 20:00:52.098+03	1	2	12403	\N
37215	info@puremedcareclinic.com	Information Desk	f	t	2025-09-01 20:00:52.108+03	2025-09-01 20:00:52.108+03	2	2	12403	\N
37216	P.O BOX 712-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:52.119+03	2025-09-01 20:00:52.119+03	14	2	12403	\N
37217	+254700000000	Facility Manager	t	t	2025-09-01 20:00:53.543+03	2025-09-01 20:00:53.543+03	1	2	12404	\N
37218	info@kianjokomamuunganoco.com	Information Desk	f	t	2025-09-01 20:00:53.55+03	2025-09-01 20:00:53.55+03	2	2	12404	\N
37219	P.O BOX 2162-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 15EMBU LICENCED		f	t	2025-09-01 20:00:53.561+03	2025-09-01 20:00:53.561+03	14	2	12404	\N
37220	+254700000000	Facility Manager	t	t	2025-09-01 20:00:55.441+03	2025-09-01 20:00:55.441+03	1	2	12405	\N
37221	info@frevanehospital.com	Information Desk	f	t	2025-09-01 20:00:55.451+03	2025-09-01 20:00:55.452+03	2	2	12405	\N
37222	P.O BOX 755-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 50EMBU LICENCED		f	t	2025-09-01 20:00:55.471+03	2025-09-01 20:00:55.471+03	14	2	12405	\N
37223	+254700000000	Facility Manager	t	t	2025-09-01 20:00:56.781+03	2025-09-01 20:00:56.781+03	1	2	12406	\N
37224	info@mercymedicalclinicem.com	Information Desk	f	t	2025-09-01 20:00:56.789+03	2025-09-01 20:00:56.789+03	2	2	12406	\N
37225	P.O BOX 1065-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:00:56.796+03	2025-09-01 20:00:56.796+03	14	2	12406	\N
37226	+254700000000	Facility Manager	t	t	2025-09-01 20:00:56.893+03	2025-09-01 20:00:56.893+03	1	2	12407	\N
37227	info@st.judemedicalcare.com	Information Desk	f	t	2025-09-01 20:00:56.899+03	2025-09-01 20:00:56.899+03	2	2	12407	\N
37228	P.O BOX 205-60100 EMBU NURSING HOME Private LEVEL 3B 15EMBU LICENCED		f	t	2025-09-01 20:00:56.907+03	2025-09-01 20:00:56.907+03	14	2	12407	\N
37229	+254700000000	Facility Manager	t	t	2025-09-01 20:00:57.033+03	2025-09-01 20:00:57.033+03	1	2	12408	\N
37230	info@generationandvisiona.com	Information Desk	f	t	2025-09-01 20:00:57.044+03	2025-09-01 20:00:57.044+03	2	2	12408	\N
37231	P.O BOX 28760-00200 NAIROBI NURSING HOME Private LEVEL 3B 35EMBU LICENCED		f	t	2025-09-01 20:00:57.058+03	2025-09-01 20:00:57.058+03	14	2	12408	\N
37232	+254700000000	Facility Manager	t	t	2025-09-01 20:00:59.136+03	2025-09-01 20:00:59.136+03	1	2	12409	\N
37233	info@mounthermonmedicalce.com	Information Desk	f	t	2025-09-01 20:00:59.148+03	2025-09-01 20:00:59.148+03	2	2	12409	\N
37234	P.O BOX 2676-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED		f	t	2025-09-01 20:00:59.156+03	2025-09-01 20:00:59.156+03	14	2	12409	\N
37235	+254700000000	Facility Manager	t	t	2025-09-01 20:01:00.925+03	2025-09-01 20:01:00.925+03	1	2	12410	\N
37236	info@mariariebenzermedica.com	Information Desk	f	t	2025-09-01 20:01:00.941+03	2025-09-01 20:01:00.941+03	2	2	12410	\N
37237	P.O BOX 85845-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:00.954+03	2025-09-01 20:01:00.954+03	14	2	12410	\N
37238	+254700000000	Facility Manager	t	t	2025-09-01 20:01:02.502+03	2025-09-01 20:01:02.502+03	1	2	12411	\N
37239	info@amazedentallimited.com	Information Desk	f	t	2025-09-01 20:01:02.511+03	2025-09-01 20:01:02.511+03	2	2	12411	\N
37240	P.O BOX 1529-60100 EMBU DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:02.52+03	2025-09-01 20:01:02.52+03	14	2	12411	\N
37241	+254700000000	Facility Manager	t	t	2025-09-01 20:01:04.048+03	2025-09-01 20:01:04.048+03	1	2	12412	\N
37242	info@highrisehealthcarese.com	Information Desk	f	t	2025-09-01 20:01:04.055+03	2025-09-01 20:01:04.055+03	2	2	12412	\N
37243	P.O BOX 254716153318-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:04.064+03	2025-09-01 20:01:04.064+03	14	2	12412	\N
37244	+254700000000	Facility Manager	t	t	2025-09-01 20:01:05.575+03	2025-09-01 20:01:05.575+03	1	2	12413	\N
37245	info@greenspringsmedicalm.com	Information Desk	f	t	2025-09-01 20:01:05.585+03	2025-09-01 20:01:05.585+03	2	2	12413	\N
37246	P.O BOX 1002-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:05.593+03	2025-09-01 20:01:05.593+03	14	2	12413	\N
37247	+254700000000	Facility Manager	t	t	2025-09-01 20:01:07.366+03	2025-09-01 20:01:07.366+03	1	2	12414	\N
37248	info@royalsmilesdentalcli.com	Information Desk	f	t	2025-09-01 20:01:07.375+03	2025-09-01 20:01:07.375+03	2	2	12414	\N
37249	P.O BOX 510-60100 EMBU DENTAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:07.383+03	2025-09-01 20:01:07.383+03	14	2	12414	\N
37250	+254700000000	Facility Manager	t	t	2025-09-01 20:01:08.793+03	2025-09-01 20:01:08.793+03	1	2	12415	\N
37251	info@grantondollynursingh.com	Information Desk	f	t	2025-09-01 20:01:08.8+03	2025-09-01 20:01:08.8+03	2	2	12415	\N
37252	P.O BOX 109-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 40EMBU LICENCED		f	t	2025-09-01 20:01:08.807+03	2025-09-01 20:01:08.807+03	14	2	12415	\N
37253	+254700000000	Facility Manager	t	t	2025-09-01 20:01:10.229+03	2025-09-01 20:01:10.229+03	1	2	12416	\N
37254	info@kiamberemedicalhealt.com	Information Desk	f	t	2025-09-01 20:01:10.235+03	2025-09-01 20:01:10.235+03	2	2	12416	\N
37255	P.O BOX 140-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 34EMBU LICENCED		f	t	2025-09-01 20:01:10.242+03	2025-09-01 20:01:10.242+03	14	2	12416	\N
37256	+254700000000	Facility Manager	t	t	2025-09-01 20:01:12.279+03	2025-09-01 20:01:12.279+03	1	2	12417	\N
37257	info@nairobiradiotherapyc.com	Information Desk	f	t	2025-09-01 20:01:12.286+03	2025-09-01 20:01:12.286+03	2	2	12417	\N
37258	P.O BOX 3280-00506 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED		f	t	2025-09-01 20:01:12.295+03	2025-09-01 20:01:12.295+03	14	2	12417	\N
37259	+254700000000	Facility Manager	t	t	2025-09-01 20:01:13.945+03	2025-09-01 20:01:13.945+03	1	2	12418	\N
37260	info@patocaremedicalcentr.com	Information Desk	f	t	2025-09-01 20:01:13.954+03	2025-09-01 20:01:13.954+03	2	2	12418	\N
37261	P.O BOX 84-10303 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:13.961+03	2025-09-01 20:01:13.961+03	14	2	12418	\N
37262	+254700000000	Facility Manager	t	t	2025-09-01 20:01:15.294+03	2025-09-01 20:01:15.294+03	1	2	12419	\N
37263	info@valleyviewmedicalspe.com	Information Desk	f	t	2025-09-01 20:01:15.313+03	2025-09-01 20:01:15.313+03	2	2	12419	\N
37264	P.O BOX 2777-60100 EMBU MEDICAL CENTRE Private LEVEL 3A 0EMBU LICENCED		f	t	2025-09-01 20:01:15.326+03	2025-09-01 20:01:15.326+03	14	2	12419	\N
37265	+254700000000	Facility Manager	t	t	2025-09-01 20:01:17.272+03	2025-09-01 20:01:17.272+03	1	2	12420	\N
37266	info@tumainimedicalcentre.com	Information Desk	f	t	2025-09-01 20:01:17.281+03	2025-09-01 20:01:17.281+03	2	2	12420	\N
37267	P.O BOX 369-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:17.295+03	2025-09-01 20:01:17.295+03	14	2	12420	\N
37268	+254700000000	Facility Manager	t	t	2025-09-01 20:01:18.778+03	2025-09-01 20:01:18.778+03	1	2	12421	\N
37269	info@mbuvoriprimemedicalc.com	Information Desk	f	t	2025-09-01 20:01:18.785+03	2025-09-01 20:01:18.785+03	2	2	12421	\N
37270	P.O BOX 591-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:18.792+03	2025-09-01 20:01:18.792+03	14	2	12421	\N
37271	+254700000000	Facility Manager	t	t	2025-09-01 20:01:20.559+03	2025-09-01 20:01:20.559+03	1	2	12422	\N
37272	info@marinimedicalcentrel.com	Information Desk	f	t	2025-09-01 20:01:20.577+03	2025-09-01 20:01:20.577+03	2	2	12422	\N
37273	P.O BOX 35-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:20.585+03	2025-09-01 20:01:20.585+03	14	2	12422	\N
37274	+254700000000	Facility Manager	t	t	2025-09-01 20:01:22.021+03	2025-09-01 20:01:22.022+03	1	2	12423	\N
37275	info@cynerdhealthcaregrou.com	Information Desk	f	t	2025-09-01 20:01:22.03+03	2025-09-01 20:01:22.03+03	2	2	12423	\N
37276	P.O BOX 1217-60100 EMBU NURSING HOME Private LEVEL 3B 45EMBU LICENCED		f	t	2025-09-01 20:01:22.038+03	2025-09-01 20:01:22.038+03	14	2	12423	\N
37277	+254700000000	Facility Manager	t	t	2025-09-01 20:01:23.63+03	2025-09-01 20:01:23.63+03	1	2	12424	\N
37278	info@magnificentmedicalce.com	Information Desk	f	t	2025-09-01 20:01:23.637+03	2025-09-01 20:01:23.637+03	2	2	12424	\N
37279	P.O BOX 280-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:23.644+03	2025-09-01 20:01:23.644+03	14	2	12424	\N
37280	+254700000000	Facility Manager	t	t	2025-09-01 20:01:24.855+03	2025-09-01 20:01:24.855+03	1	2	12425	\N
37281	info@serenityhomesrehabil.com	Information Desk	f	t	2025-09-01 20:01:24.863+03	2025-09-01 20:01:24.863+03	2	2	12425	\N
37282	P.O BOX 660-60100 EMBU NURSING HOME Private LEVEL 3B 50EMBU LICENCED		f	t	2025-09-01 20:01:24.872+03	2025-09-01 20:01:24.872+03	14	2	12425	\N
37283	+254700000000	Facility Manager	t	t	2025-09-01 20:01:26.709+03	2025-09-01 20:01:26.709+03	1	2	12426	\N
37284	info@pleromamedicalcentre.com	Information Desk	f	t	2025-09-01 20:01:26.718+03	2025-09-01 20:01:26.718+03	2	2	12426	\N
37285	P.O BOX 2546-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:26.726+03	2025-09-01 20:01:26.726+03	14	2	12426	\N
37286	+254700000000	Facility Manager	t	t	2025-09-01 20:01:28.115+03	2025-09-01 20:01:28.115+03	1	2	12427	\N
37287	info@vicopticeyecliniclim.com	Information Desk	f	t	2025-09-01 20:01:28.122+03	2025-09-01 20:01:28.122+03	2	2	12427	\N
37288	P.O BOX 143-60100 EMBU EYE CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:28.128+03	2025-09-01 20:01:28.128+03	14	2	12427	\N
37289	+254700000000	Facility Manager	t	t	2025-09-01 20:01:29.59+03	2025-09-01 20:01:29.59+03	1	2	12428	\N
37290	info@imarahospitalembu.com	Information Desk	f	t	2025-09-01 20:01:29.599+03	2025-09-01 20:01:29.599+03	2	2	12428	\N
37291	P.O BOX 1446-60100 EMBU HOSPITAL LEVEL 4INTERNSHIP TRAINING CENTRECOUNTY HOSPITAL Private LEVEL 4 90EMBU LICENCED		f	t	2025-09-01 20:01:29.608+03	2025-09-01 20:01:29.608+03	14	2	12428	\N
37292	+254700000000	Facility Manager	t	t	2025-09-01 20:01:30.792+03	2025-09-01 20:01:30.792+03	1	2	12429	\N
37293	info@loyaltyhopeclinic.com	Information Desk	f	t	2025-09-01 20:01:30.805+03	2025-09-01 20:01:30.805+03	2	2	12429	\N
37294	P.O BOX 130-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:30.813+03	2025-09-01 20:01:30.813+03	14	2	12429	\N
37295	+254700000000	Facility Manager	t	t	2025-09-01 20:01:31.992+03	2025-09-01 20:01:31.992+03	1	2	12430	\N
37296	info@njukirimedicalcentre.com	Information Desk	f	t	2025-09-01 20:01:32.001+03	2025-09-01 20:01:32.001+03	2	2	12430	\N
37297	P.O BOX 850-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:32.009+03	2025-09-01 20:01:32.009+03	14	2	12430	\N
37298	+254700000000	Facility Manager	t	t	2025-09-01 20:01:33.132+03	2025-09-01 20:01:33.132+03	1	2	12431	\N
37299	info@embupremierphysician.com	Information Desk	f	t	2025-09-01 20:01:33.139+03	2025-09-01 20:01:33.139+03	2	2	12431	\N
37300	P.O BOX 2586-00100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:33.147+03	2025-09-01 20:01:33.147+03	14	2	12431	\N
37301	+254700000000	Facility Manager	t	t	2025-09-01 20:01:34.796+03	2025-09-01 20:01:34.796+03	1	2	12432	\N
37302	info@theparadoxhospitals.com	Information Desk	f	t	2025-09-01 20:01:34.805+03	2025-09-01 20:01:34.805+03	2	2	12432	\N
37303	P.O BOX 618-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:34.814+03	2025-09-01 20:01:34.814+03	14	2	12432	\N
37304	+254700000000	Facility Manager	t	t	2025-09-01 20:01:36.541+03	2025-09-01 20:01:36.541+03	1	2	12433	\N
37305	info@kiritirifuneralhome.com	Information Desk	f	t	2025-09-01 20:01:36.548+03	2025-09-01 20:01:36.548+03	2	2	12433	\N
37306	P.O BOX 2851-60100 EMBU FUNERAL HOME (STAND ALONE) Private LEVEL 3A 30EMBU LICENCED		f	t	2025-09-01 20:01:36.554+03	2025-09-01 20:01:36.554+03	14	2	12433	\N
37307	+254700000000	Facility Manager	t	t	2025-09-01 20:01:38.019+03	2025-09-01 20:01:38.019+03	1	2	12434	\N
37308	info@forealtorshospitallt.com	Information Desk	f	t	2025-09-01 20:01:38.028+03	2025-09-01 20:01:38.028+03	2	2	12434	\N
37309	P.O BOX 278-60103 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:38.034+03	2025-09-01 20:01:38.034+03	14	2	12434	\N
37310	+254700000000	Facility Manager	t	t	2025-09-01 20:01:39.383+03	2025-09-01 20:01:39.383+03	1	2	12435	\N
37311	info@waltermedicalanddent.com	Information Desk	f	t	2025-09-01 20:01:39.4+03	2025-09-01 20:01:39.4+03	2	2	12435	\N
37312	P.O BOX 1333-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:39.421+03	2025-09-01 20:01:39.421+03	14	2	12435	\N
37313	+254700000000	Facility Manager	t	t	2025-09-01 20:01:40.745+03	2025-09-01 20:01:40.745+03	1	2	12436	\N
37314	info@framarymedicalcentre.com	Information Desk	f	t	2025-09-01 20:01:40.753+03	2025-09-01 20:01:40.753+03	2	2	12436	\N
37315	P.O BOX 33-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:40.761+03	2025-09-01 20:01:40.761+03	14	2	12436	\N
37316	+254700000000	Facility Manager	t	t	2025-09-01 20:01:42.022+03	2025-09-01 20:01:42.022+03	1	2	12437	\N
37317	info@ericaremedicalandphy.com	Information Desk	f	t	2025-09-01 20:01:42.029+03	2025-09-01 20:01:42.029+03	2	2	12437	\N
37318	P.O BOX 29-60125 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:42.038+03	2025-09-01 20:01:42.038+03	14	2	12437	\N
37319	+254700000000	Facility Manager	t	t	2025-09-01 20:01:43.405+03	2025-09-01 20:01:43.405+03	1	2	12438	\N
37320	info@emmanuelmekamedicalc.com	Information Desk	f	t	2025-09-01 20:01:43.414+03	2025-09-01 20:01:43.414+03	2	2	12438	\N
37321	P.O BOX 168-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:43.421+03	2025-09-01 20:01:43.421+03	14	2	12438	\N
37322	+254700000000	Facility Manager	t	t	2025-09-01 20:01:45.225+03	2025-09-01 20:01:45.225+03	1	2	12439	\N
37323	info@neemauniversalhealth.com	Information Desk	f	t	2025-09-01 20:01:45.233+03	2025-09-01 20:01:45.233+03	2	2	12439	\N
37324	P.O BOX 2228-60100 EMBU HOSPITAL LEVEL 4 Private LEVEL 4 71EMBU LICENCED		f	t	2025-09-01 20:01:45.24+03	2025-09-01 20:01:45.24+03	14	2	12439	\N
37325	+254700000000	Facility Manager	t	t	2025-09-01 20:01:46.907+03	2025-09-01 20:01:46.907+03	1	2	12440	\N
37326	info@fountainofhopemedica.com	Information Desk	f	t	2025-09-01 20:01:46.916+03	2025-09-01 20:01:46.916+03	2	2	12440	\N
37327	P.O BOX 1905-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:46.923+03	2025-09-01 20:01:46.923+03	14	2	12440	\N
37328	+254700000000	Facility Manager	t	t	2025-09-01 20:01:47.017+03	2025-09-01 20:01:47.017+03	1	2	12441	\N
37329	info@kamiujunctioncommuni.com	Information Desk	f	t	2025-09-01 20:01:47.024+03	2025-09-01 20:01:47.024+03	2	2	12441	\N
37330	P.O BOX 33-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:47.031+03	2025-09-01 20:01:47.031+03	14	2	12441	\N
37331	+254700000000	Facility Manager	t	t	2025-09-01 20:01:48.511+03	2025-09-01 20:01:48.511+03	1	2	12442	\N
37332	info@graceviewmedicalcent.com	Information Desk	f	t	2025-09-01 20:01:48.518+03	2025-09-01 20:01:48.518+03	2	2	12442	\N
37333	P.O BOX 33-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:48.524+03	2025-09-01 20:01:48.524+03	14	2	12442	\N
37334	+254700000000	Facility Manager	t	t	2025-09-01 20:01:49.828+03	2025-09-01 20:01:49.828+03	1	2	12443	\N
37335	info@kengengitarustaffcli.com	Information Desk	f	t	2025-09-01 20:01:49.84+03	2025-09-01 20:01:49.84+03	2	2	12443	\N
37336	P.O BOX 205-60100 EMBU MEDICAL CLINIC Private LEVEL 2 0EMBU LICENCED		f	t	2025-09-01 20:01:49.859+03	2025-09-01 20:01:49.859+03	14	2	12443	\N
37337	+254700000000	Facility Manager	t	t	2025-09-01 20:01:51.316+03	2025-09-01 20:01:51.316+03	1	2	12444	\N
37338	info@garissamotherandchil.com	Information Desk	f	t	2025-09-01 20:01:51.326+03	2025-09-01 20:01:51.326+03	2	2	12444	\N
37339	P.O BOX 547-- GARISSA NURSING HOME Private LEVEL 3B 14GARISSA LICENCED		f	t	2025-09-01 20:01:51.337+03	2025-09-01 20:01:51.337+03	14	2	12444	\N
37340	+254700000000	Facility Manager	t	t	2025-09-01 20:01:52.893+03	2025-09-01 20:01:52.893+03	1	2	12445	\N
37341	info@towbamedicalcare.com	Information Desk	f	t	2025-09-01 20:01:52.9+03	2025-09-01 20:01:52.9+03	2	2	12445	\N
37342	P.O BOX 445-70100 GARISSA HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 0GARISSA LICENCED		f	t	2025-09-01 20:01:52.908+03	2025-09-01 20:01:52.908+03	14	2	12445	\N
37343	+254700000000	Facility Manager	t	t	2025-09-01 20:01:54.11+03	2025-09-01 20:01:54.11+03	1	2	12446	\N
37344	info@bullahagardispensary.com	Information Desk	f	t	2025-09-01 20:01:54.12+03	2025-09-01 20:01:54.12+03	2	2	12446	\N
37345	P.O BOX 808-70100 GARISSA DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:01:54.128+03	2025-09-01 20:01:54.128+03	14	2	12446	\N
37346	+254700000000	Facility Manager	t	t	2025-09-01 20:01:54.222+03	2025-09-01 20:01:54.222+03	1	2	12447	\N
37347	info@iommigrationassesmen.com	Information Desk	f	t	2025-09-01 20:01:54.241+03	2025-09-01 20:01:54.241+03	2	2	12447	\N
37348	P.O BOX 55040-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:01:54.249+03	2025-09-01 20:01:54.249+03	14	2	12447	\N
37349	+254700000000	Facility Manager	t	t	2025-09-01 20:01:56.127+03	2025-09-01 20:01:56.127+03	1	2	12448	\N
37350	info@garissanursinghome.com	Information Desk	f	t	2025-09-01 20:01:56.134+03	2025-09-01 20:01:56.134+03	2	2	12448	\N
37351	P.O BOX 269-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 50GARISSA LICENCED		f	t	2025-09-01 20:01:56.142+03	2025-09-01 20:01:56.142+03	14	2	12448	\N
37352	+254700000000	Facility Manager	t	t	2025-09-01 20:01:56.325+03	2025-09-01 20:01:56.325+03	1	2	12449	\N
37353	info@simahomchfpclinic.com	Information Desk	f	t	2025-09-01 20:01:56.335+03	2025-09-01 20:01:56.335+03	2	2	12449	\N
37354	P.O BOX 545-70100 GARISSA HEALTH CENTRE Private LEVEL 3B 14GARISSA LICENCED		f	t	2025-09-01 20:01:56.35+03	2025-09-01 20:01:56.35+03	14	2	12449	\N
37355	+254700000000	Facility Manager	t	t	2025-09-01 20:01:57.781+03	2025-09-01 20:01:57.781+03	1	2	12450	\N
37356	info@noorhilacpharmaceuti.com	Information Desk	f	t	2025-09-01 20:01:57.791+03	2025-09-01 20:01:57.791+03	2	2	12450	\N
37357	P.O BOX 197-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 3GARISSA LICENCED		f	t	2025-09-01 20:01:57.799+03	2025-09-01 20:01:57.799+03	14	2	12450	\N
37358	+254700000000	Facility Manager	t	t	2025-09-01 20:01:59.231+03	2025-09-01 20:01:59.231+03	1	2	12451	\N
37359	info@excelhealthservicesg.com	Information Desk	f	t	2025-09-01 20:01:59.239+03	2025-09-01 20:01:59.239+03	2	2	12451	\N
37360	P.O BOX 501-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED		f	t	2025-09-01 20:01:59.247+03	2025-09-01 20:01:59.247+03	14	2	12451	\N
37361	+254700000000	Facility Manager	t	t	2025-09-01 20:02:00.888+03	2025-09-01 20:02:00.888+03	1	2	12452	\N
37362	info@medinamedicarehospit.com	Information Desk	f	t	2025-09-01 20:02:00.896+03	2025-09-01 20:02:00.896+03	2	2	12452	\N
37363	P.O BOX 126-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 50GARISSA LICENCED		f	t	2025-09-01 20:02:00.903+03	2025-09-01 20:02:00.903+03	14	2	12452	\N
37364	+254700000000	Facility Manager	t	t	2025-09-01 20:02:02.666+03	2025-09-01 20:02:02.666+03	1	2	12453	\N
37365	info@tawheedcommunitynurs.com	Information Desk	f	t	2025-09-01 20:02:02.673+03	2025-09-01 20:02:02.673+03	2	2	12453	\N
37366	P.O BOX 1419-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 52GARISSA LICENCED		f	t	2025-09-01 20:02:02.682+03	2025-09-01 20:02:02.682+03	14	2	12453	\N
37367	+254700000000	Facility Manager	t	t	2025-09-01 20:02:03.985+03	2025-09-01 20:02:03.985+03	1	2	12454	\N
37368	info@northeasternmedicalc.com	Information Desk	f	t	2025-09-01 20:02:03.992+03	2025-09-01 20:02:03.992+03	2	2	12454	\N
37369	P.O BOX 720-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:02:04.001+03	2025-09-01 20:02:04.001+03	14	2	12454	\N
37370	+254700000000	Facility Manager	t	t	2025-09-01 20:02:05.17+03	2025-09-01 20:02:05.17+03	1	2	12455	\N
37371	info@medinahospital.com	Information Desk	f	t	2025-09-01 20:02:05.185+03	2025-09-01 20:02:05.185+03	2	2	12455	\N
37372	P.O BOX 126-70100 GARISSA Hospital Level 5 Private LEVEL 5 110 GARISSA LICENCED		f	t	2025-09-01 20:02:05.201+03	2025-09-01 20:02:05.201+03	14	2	12455	\N
37373	+254700000000	Facility Manager	t	t	2025-09-01 20:02:05.37+03	2025-09-01 20:02:05.37+03	1	2	12456	\N
37374	info@womensinitiativeheal.com	Information Desk	f	t	2025-09-01 20:02:05.382+03	2025-09-01 20:02:05.382+03	2	2	12456	\N
37375	P.O BOX 545-70100 GARISSA HEALTH CENTRE Private LEVEL 3B 10GARISSA LICENCED		f	t	2025-09-01 20:02:05.394+03	2025-09-01 20:02:05.394+03	14	2	12456	\N
37376	+254700000000	Facility Manager	t	t	2025-09-01 20:02:07.052+03	2025-09-01 20:02:07.052+03	1	2	12457	\N
37377	info@alliancemedicalcentr.com	Information Desk	f	t	2025-09-01 20:02:07.059+03	2025-09-01 20:02:07.059+03	2	2	12457	\N
37378	P.O BOX 1808-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 60GARISSA LICENCED		f	t	2025-09-01 20:02:07.065+03	2025-09-01 20:02:07.065+03	14	2	12457	\N
37379	+254700000000	Facility Manager	t	t	2025-09-01 20:02:08.631+03	2025-09-01 20:02:08.631+03	1	2	12458	\N
37380	info@cosgurowhealthcareli.com	Information Desk	f	t	2025-09-01 20:02:08.64+03	2025-09-01 20:02:08.64+03	2	2	12458	\N
37381	P.O BOX 176-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 16GARISSA LICENCED		f	t	2025-09-01 20:02:08.653+03	2025-09-01 20:02:08.653+03	14	2	12458	\N
37382	+254700000000	Facility Manager	t	t	2025-09-01 20:02:09.979+03	2025-09-01 20:02:09.979+03	1	2	12459	\N
37383	info@almaqdismedicalcentr.com	Information Desk	f	t	2025-09-01 20:02:09.988+03	2025-09-01 20:02:09.988+03	2	2	12459	\N
37384	P.O BOX 470-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 42GARISSA LICENCED		f	t	2025-09-01 20:02:09.994+03	2025-09-01 20:02:09.994+03	14	2	12459	\N
37385	+254700000000	Facility Manager	t	t	2025-09-01 20:02:11.077+03	2025-09-01 20:02:11.077+03	1	2	12460	\N
37386	info@alaminmedicallabarat.com	Information Desk	f	t	2025-09-01 20:02:11.084+03	2025-09-01 20:02:11.084+03	2	2	12460	\N
37387	P.O BOX 29-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:11.093+03	2025-09-01 20:02:11.093+03	14	2	12460	\N
37388	+254700000000	Facility Manager	t	t	2025-09-01 20:02:12.512+03	2025-09-01 20:02:12.512+03	1	2	12461	\N
37389	info@garissachildrenshosp.com	Information Desk	f	t	2025-09-01 20:02:12.522+03	2025-09-01 20:02:12.522+03	2	2	12461	\N
37390	P.O BOX 514-70100 GARISSA NURSING HOME Private LEVEL 3B 16GARISSA LICENCED		f	t	2025-09-01 20:02:12.532+03	2025-09-01 20:02:12.532+03	14	2	12461	\N
37391	+254700000000	Facility Manager	t	t	2025-09-01 20:02:14.377+03	2025-09-01 20:02:14.377+03	1	2	12462	\N
37392	info@countmedicalanddiagn.com	Information Desk	f	t	2025-09-01 20:02:14.392+03	2025-09-01 20:02:14.392+03	2	2	12462	\N
37393	P.O BOX 1538-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 45GARISSA LICENCED		f	t	2025-09-01 20:02:14.401+03	2025-09-01 20:02:14.401+03	14	2	12462	\N
37394	+254700000000	Facility Manager	t	t	2025-09-01 20:02:15.772+03	2025-09-01 20:02:15.772+03	1	2	12463	\N
37395	info@zensturioncommunityh.com	Information Desk	f	t	2025-09-01 20:02:15.783+03	2025-09-01 20:02:15.783+03	2	2	12463	\N
37396	P.O BOX 151-60103 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:15.798+03	2025-09-01 20:02:15.798+03	14	2	12463	\N
37397	+254700000000	Facility Manager	t	t	2025-09-01 20:02:17.611+03	2025-09-01 20:02:17.611+03	1	2	12464	\N
37398	info@afnaanhealthcareserv.com	Information Desk	f	t	2025-09-01 20:02:17.617+03	2025-09-01 20:02:17.617+03	2	2	12464	\N
37399	P.O BOX 486-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 11GARISSA LICENCED		f	t	2025-09-01 20:02:17.623+03	2025-09-01 20:02:17.623+03	14	2	12464	\N
37400	+254700000000	Facility Manager	t	t	2025-09-01 20:02:18.983+03	2025-09-01 20:02:18.983+03	1	2	12465	\N
37401	info@hilwamedicalcentre.com	Information Desk	f	t	2025-09-01 20:02:18.991+03	2025-09-01 20:02:18.991+03	2	2	12465	\N
37402	P.O BOX 523-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:19+03	2025-09-01 20:02:19+03	14	2	12465	\N
37403	+254700000000	Facility Manager	t	t	2025-09-01 20:02:19.071+03	2025-09-01 20:02:19.071+03	1	2	12466	\N
37404	info@albushramedicalcentr.com	Information Desk	f	t	2025-09-01 20:02:19.079+03	2025-09-01 20:02:19.079+03	2	2	12466	\N
37405	P.O BOX 15 - GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:19.086+03	2025-09-01 20:02:19.086+03	14	2	12466	\N
37406	+254700000000	Facility Manager	t	t	2025-09-01 20:02:19.173+03	2025-09-01 20:02:19.173+03	1	2	12467	\N
37407	info@medinamedicarehospit.com	Information Desk	f	t	2025-09-01 20:02:19.181+03	2025-09-01 20:02:19.181+03	2	2	12467	\N
37408	P.O BOX 126-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED		f	t	2025-09-01 20:02:19.187+03	2025-09-01 20:02:19.187+03	14	2	12467	\N
37409	+254700000000	Facility Manager	t	t	2025-09-01 20:02:20.819+03	2025-09-01 20:02:20.819+03	1	2	12468	\N
37410	info@familyfirstmedicalce.com	Information Desk	f	t	2025-09-01 20:02:20.838+03	2025-09-01 20:02:20.838+03	2	2	12468	\N
37411	P.O BOX 1412-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED		f	t	2025-09-01 20:02:20.861+03	2025-09-01 20:02:20.861+03	14	2	12468	\N
37412	+254700000000	Facility Manager	t	t	2025-09-01 20:02:22.034+03	2025-09-01 20:02:22.034+03	1	2	12469	\N
37413	info@northgatehospitallim.com	Information Desk	f	t	2025-09-01 20:02:22.042+03	2025-09-01 20:02:22.042+03	2	2	12469	\N
37414	P.O BOX 1112-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 50GARISSA LICENCED		f	t	2025-09-01 20:02:22.049+03	2025-09-01 20:02:22.049+03	14	2	12469	\N
37415	+254700000000	Facility Manager	t	t	2025-09-01 20:02:23.205+03	2025-09-01 20:02:23.205+03	1	2	12470	\N
37416	info@jihanmedicalcentre.com	Information Desk	f	t	2025-09-01 20:02:23.214+03	2025-09-01 20:02:23.214+03	2	2	12470	\N
37417	P.O BOX 1270-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:23.222+03	2025-09-01 20:02:23.222+03	14	2	12470	\N
37418	+254700000000	Facility Manager	t	t	2025-09-01 20:02:24.245+03	2025-09-01 20:02:24.245+03	1	2	12471	\N
37419	info@garissadoctorsplaza.com	Information Desk	f	t	2025-09-01 20:02:24.254+03	2025-09-01 20:02:24.254+03	2	2	12471	\N
37420	P.O BOX 1558-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 52GARISSA LICENCED		f	t	2025-09-01 20:02:24.26+03	2025-09-01 20:02:24.26+03	14	2	12471	\N
37421	+254700000000	Facility Manager	t	t	2025-09-01 20:02:25.852+03	2025-09-01 20:02:25.852+03	1	2	12472	\N
37422	info@tasneemmedicalclinic.com	Information Desk	f	t	2025-09-01 20:02:25.859+03	2025-09-01 20:02:25.859+03	2	2	12472	\N
37423	P.O BOX 983-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:25.865+03	2025-09-01 20:02:25.865+03	14	2	12472	\N
37424	+254700000000	Facility Manager	t	t	2025-09-01 20:02:27.172+03	2025-09-01 20:02:27.172+03	1	2	12473	\N
37425	info@alrashadmedicalcentr.com	Information Desk	f	t	2025-09-01 20:02:27.18+03	2025-09-01 20:02:27.18+03	2	2	12473	\N
37426	P.O BOX 60-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:27.188+03	2025-09-01 20:02:27.188+03	14	2	12473	\N
37427	+254700000000	Facility Manager	t	t	2025-09-01 20:02:28.418+03	2025-09-01 20:02:28.418+03	1	2	12474	\N
37428	info@sunnahealthcaredenta.com	Information Desk	f	t	2025-09-01 20:02:28.426+03	2025-09-01 20:02:28.426+03	2	2	12474	\N
37429	P.O BOX 9279-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED		f	t	2025-09-01 20:02:28.433+03	2025-09-01 20:02:28.433+03	14	2	12474	\N
37430	+254700000000	Facility Manager	t	t	2025-09-01 20:02:29.724+03	2025-09-01 20:02:29.724+03	1	2	12475	\N
37431	info@ankaramedicalcenterl.com	Information Desk	f	t	2025-09-01 20:02:29.738+03	2025-09-01 20:02:29.738+03	2	2	12475	\N
37432	P.O BOX 973-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:02:29.747+03	2025-09-01 20:02:29.747+03	14	2	12475	\N
37433	+254700000000	Facility Manager	t	t	2025-09-01 20:02:31.362+03	2025-09-01 20:02:31.362+03	1	2	12476	\N
37434	info@garissaentmedicalcen.com	Information Desk	f	t	2025-09-01 20:02:31.376+03	2025-09-01 20:02:31.376+03	2	2	12476	\N
37435	P.O BOX 1857-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 27GARISSA LICENCED		f	t	2025-09-01 20:02:31.391+03	2025-09-01 20:02:31.391+03	14	2	12476	\N
37436	+254700000000	Facility Manager	t	t	2025-09-01 20:02:32.622+03	2025-09-01 20:02:32.622+03	1	2	12477	\N
37437	info@anfacnursinghome.com	Information Desk	f	t	2025-09-01 20:02:32.631+03	2025-09-01 20:02:32.631+03	2	2	12477	\N
37438	P.O BOX 365-70100 GARISSA NURSING HOME Private LEVEL 3B 12GARISSA LICENCED		f	t	2025-09-01 20:02:32.64+03	2025-09-01 20:02:32.64+03	14	2	12477	\N
37439	+254700000000	Facility Manager	t	t	2025-09-01 20:02:33.755+03	2025-09-01 20:02:33.755+03	1	2	12478	\N
37440	info@masalanidiagnosticli.com	Information Desk	f	t	2025-09-01 20:02:33.763+03	2025-09-01 20:02:33.763+03	2	2	12478	\N
37441	P.O BOX 65-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED		f	t	2025-09-01 20:02:33.769+03	2025-09-01 20:02:33.769+03	14	2	12478	\N
37442	+254700000000	Facility Manager	t	t	2025-09-01 20:02:35.126+03	2025-09-01 20:02:35.126+03	1	2	12479	\N
37443	info@alqudusmedicalcentre.com	Information Desk	f	t	2025-09-01 20:02:35.132+03	2025-09-01 20:02:35.132+03	2	2	12479	\N
37444	P.O BOX 953-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:02:35.139+03	2025-09-01 20:02:35.139+03	14	2	12479	\N
37445	+254700000000	Facility Manager	t	t	2025-09-01 20:02:35.221+03	2025-09-01 20:02:35.221+03	1	2	12480	\N
37446	info@madogashemedicalserv.com	Information Desk	f	t	2025-09-01 20:02:35.227+03	2025-09-01 20:02:35.227+03	2	2	12480	\N
37447	P.O BOX 23-70102 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED		f	t	2025-09-01 20:02:35.234+03	2025-09-01 20:02:35.234+03	14	2	12480	\N
37448	+254700000000	Facility Manager	t	t	2025-09-01 20:02:36.749+03	2025-09-01 20:02:36.749+03	1	2	12481	\N
37449	info@modogashenursinghome.com	Information Desk	f	t	2025-09-01 20:02:36.756+03	2025-09-01 20:02:36.756+03	2	2	12481	\N
37450	P.O BOX 73-70100 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED		f	t	2025-09-01 20:02:36.763+03	2025-09-01 20:02:36.763+03	14	2	12481	\N
37451	+254700000000	Facility Manager	t	t	2025-09-01 20:02:36.87+03	2025-09-01 20:02:36.87+03	1	2	12482	\N
37452	info@garissanursinghomean.com	Information Desk	f	t	2025-09-01 20:02:36.877+03	2025-09-01 20:02:36.877+03	2	2	12482	\N
37453	P.O BOX 269-70100 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED		f	t	2025-09-01 20:02:36.884+03	2025-09-01 20:02:36.884+03	14	2	12482	\N
37454	+254700000000	Facility Manager	t	t	2025-09-01 20:02:38.112+03	2025-09-01 20:02:38.112+03	1	2	12483	\N
37455	info@antaliyahospitallimi.com	Information Desk	f	t	2025-09-01 20:02:38.12+03	2025-09-01 20:02:38.12+03	2	2	12483	\N
37456	P.O BOX 448-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 35GARISSA LICENCED		f	t	2025-09-01 20:02:38.127+03	2025-09-01 20:02:38.127+03	14	2	12483	\N
37457	+254700000000	Facility Manager	t	t	2025-09-01 20:02:39.314+03	2025-09-01 20:02:39.314+03	1	2	12484	\N
37458	info@dagahleymedicalhealt.com	Information Desk	f	t	2025-09-01 20:02:39.322+03	2025-09-01 20:02:39.322+03	2	2	12484	\N
37459	P.O BOX 20-70100 GARISSA NURSING HOME Private LEVEL 3B 22GARISSA LICENCED		f	t	2025-09-01 20:02:39.332+03	2025-09-01 20:02:39.332+03	14	2	12484	\N
37460	+254700000000	Facility Manager	t	t	2025-09-01 20:02:40.702+03	2025-09-01 20:02:40.702+03	1	2	12485	\N
37461	info@highgatehealthcareli.com	Information Desk	f	t	2025-09-01 20:02:40.709+03	2025-09-01 20:02:40.709+03	2	2	12485	\N
37462	P.O BOX 140-07100 GARISSA MEDICAL CENTRE Private LEVEL 3A 8GARISSA LICENCED		f	t	2025-09-01 20:02:40.716+03	2025-09-01 20:02:40.716+03	14	2	12485	\N
37463	+254700000000	Facility Manager	t	t	2025-09-01 20:02:42.508+03	2025-09-01 20:02:42.508+03	1	2	12486	\N
37464	info@sarapmedicalcentre.com	Information Desk	f	t	2025-09-01 20:02:42.516+03	2025-09-01 20:02:42.516+03	2	2	12486	\N
37465	P.O BOX 341-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 10GARISSA LICENCED		f	t	2025-09-01 20:02:42.523+03	2025-09-01 20:02:42.523+03	14	2	12486	\N
37466	+254700000000	Facility Manager	t	t	2025-09-01 20:02:43.569+03	2025-09-01 20:02:43.569+03	1	2	12487	\N
37467	info@garissaeyehospitallt.com	Information Desk	f	t	2025-09-01 20:02:43.576+03	2025-09-01 20:02:43.576+03	2	2	12487	\N
37468	P.O BOX 1474-70100 GARISSA EYE HOSPITAL LEVEL 4 Private LEVEL 4 16GARISSA LICENCED		f	t	2025-09-01 20:02:43.583+03	2025-09-01 20:02:43.583+03	14	2	12487	\N
37469	+254700000000	Facility Manager	t	t	2025-09-01 20:02:44.814+03	2025-09-01 20:02:44.814+03	1	2	12488	\N
37470	info@jamiaislamicintergra.com	Information Desk	f	t	2025-09-01 20:02:44.821+03	2025-09-01 20:02:44.821+03	2	2	12488	\N
37471	P.O BOX 126-70100 GARISSA HOSPITAL LEVEL 4 Private LEVEL 4 40GARISSA LICENCED		f	t	2025-09-01 20:02:44.828+03	2025-09-01 20:02:44.828+03	14	2	12488	\N
37472	+254700000000	Facility Manager	t	t	2025-09-01 20:02:46.329+03	2025-09-01 20:02:46.329+03	1	2	12489	\N
37473	info@hamdanmedicalcentre.com	Information Desk	f	t	2025-09-01 20:02:46.336+03	2025-09-01 20:02:46.336+03	2	2	12489	\N
37474	P.O BOX 40701- GARISSA MEDICAL CENTRE Private LEVEL 3A 14GARISSA LICENCED		f	t	2025-09-01 20:02:46.343+03	2025-09-01 20:02:46.343+03	14	2	12489	\N
37475	+254700000000	Facility Manager	t	t	2025-09-01 20:02:47.496+03	2025-09-01 20:02:47.496+03	1	2	12490	\N
37476	info@gacalbudgethospital.com	Information Desk	f	t	2025-09-01 20:02:47.512+03	2025-09-01 20:02:47.512+03	2	2	12490	\N
37477	P.O BOX 553-70100 GARISSA NURSING HOME Private LEVEL 3B 50GARISSA LICENCED		f	t	2025-09-01 20:02:47.535+03	2025-09-01 20:02:47.535+03	14	2	12490	\N
37478	+254700000000	Facility Manager	t	t	2025-09-01 20:02:48.772+03	2025-09-01 20:02:48.772+03	1	2	12491	\N
37479	info@samaramedicalcentre.com	Information Desk	f	t	2025-09-01 20:02:48.78+03	2025-09-01 20:02:48.78+03	2	2	12491	\N
37480	P.O BOX 830-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED		f	t	2025-09-01 20:02:48.786+03	2025-09-01 20:02:48.787+03	14	2	12491	\N
37481	+254700000000	Facility Manager	t	t	2025-09-01 20:02:50.28+03	2025-09-01 20:02:50.28+03	1	2	12492	\N
37482	info@aldayaxmedicalclinic.com	Information Desk	f	t	2025-09-01 20:02:50.288+03	2025-09-01 20:02:50.288+03	2	2	12492	\N
37483	P.O BOX 126-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:50.296+03	2025-09-01 20:02:50.296+03	14	2	12492	\N
37484	+254700000000	Facility Manager	t	t	2025-09-01 20:02:51.774+03	2025-09-01 20:02:51.774+03	1	2	12493	\N
37485	info@mbassymedicalcentrel.com	Information Desk	f	t	2025-09-01 20:02:51.781+03	2025-09-01 20:02:51.781+03	2	2	12493	\N
37486	P.O BOX 514-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 10GARISSA LICENCED		f	t	2025-09-01 20:02:51.788+03	2025-09-01 20:02:51.788+03	14	2	12493	\N
37487	+254700000000	Facility Manager	t	t	2025-09-01 20:02:53.057+03	2025-09-01 20:02:53.057+03	1	2	12494	\N
37488	info@stardentalclinicslim.com	Information Desk	f	t	2025-09-01 20:02:53.07+03	2025-09-01 20:02:53.07+03	2	2	12494	\N
37489	P.O BOX 7883-00610 NAIROBI DENTAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:53.085+03	2025-09-01 20:02:53.085+03	14	2	12494	\N
37490	+254700000000	Facility Manager	t	t	2025-09-01 20:02:54.346+03	2025-09-01 20:02:54.346+03	1	2	12495	\N
37491	info@tawheedmedicalclinic.com	Information Desk	f	t	2025-09-01 20:02:54.365+03	2025-09-01 20:02:54.365+03	2	2	12495	\N
37492	P.O BOX 1419-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:54.378+03	2025-09-01 20:02:54.378+03	14	2	12495	\N
37493	+254700000000	Facility Manager	t	t	2025-09-01 20:02:55.976+03	2025-09-01 20:02:55.976+03	1	2	12496	\N
37494	info@dobaleclinic.com	Information Desk	f	t	2025-09-01 20:02:55.983+03	2025-09-01 20:02:55.983+03	2	2	12496	\N
37495	P.O BOX 256-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:02:55.989+03	2025-09-01 20:02:55.989+03	14	2	12496	\N
37496	+254700000000	Facility Manager	t	t	2025-09-01 20:02:57.533+03	2025-09-01 20:02:57.533+03	1	2	12497	\N
37497	info@shifamaternalandchil.com	Information Desk	f	t	2025-09-01 20:02:57.541+03	2025-09-01 20:02:57.541+03	2	2	12497	\N
37498	P.O BOX 658-70100 GARISSA NURSING HOME Private LEVEL 3B 30GARISSA LICENCED		f	t	2025-09-01 20:02:57.547+03	2025-09-01 20:02:57.547+03	14	2	12497	\N
37499	+254700000000	Facility Manager	t	t	2025-09-01 20:02:59.448+03	2025-09-01 20:02:59.448+03	1	2	12498	\N
37500	info@nepnursingandrehabil.com	Information Desk	f	t	2025-09-01 20:02:59.456+03	2025-09-01 20:02:59.456+03	2	2	12498	\N
37501	P.O BOX 23-70100 GARISSA REHABILITATION CENTRE Private LEVEL 3A 10GARISSA LICENCED		f	t	2025-09-01 20:02:59.463+03	2025-09-01 20:02:59.463+03	14	2	12498	\N
37502	+254700000000	Facility Manager	t	t	2025-09-01 20:03:01.246+03	2025-09-01 20:03:01.246+03	1	2	12499	\N
37503	info@savannahroyalhospita.com	Information Desk	f	t	2025-09-01 20:03:01.252+03	2025-09-01 20:03:01.252+03	2	2	12499	\N
37504	P.O BOX 20617-00100 NAIROBI HOSPITAL LEVEL 4 Private LEVEL 4 65GARISSA LICENCED		f	t	2025-09-01 20:03:01.262+03	2025-09-01 20:03:01.262+03	14	2	12499	\N
37505	+254700000000	Facility Manager	t	t	2025-09-01 20:03:02.719+03	2025-09-01 20:03:02.719+03	1	2	12500	\N
37506	info@emirateshospitallimi.com	Information Desk	f	t	2025-09-01 20:03:02.726+03	2025-09-01 20:03:02.726+03	2	2	12500	\N
37507	P.O BOX 311-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED		f	t	2025-09-01 20:03:02.733+03	2025-09-01 20:03:02.733+03	14	2	12500	\N
37508	+254700000000	Facility Manager	t	t	2025-09-01 20:03:04.067+03	2025-09-01 20:03:04.067+03	1	2	12501	\N
37509	info@albaitultiibahospita.com	Information Desk	f	t	2025-09-01 20:03:04.074+03	2025-09-01 20:03:04.074+03	2	2	12501	\N
37510	P.O BOX 882-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED		f	t	2025-09-01 20:03:04.081+03	2025-09-01 20:03:04.081+03	14	2	12501	\N
37511	+254700000000	Facility Manager	t	t	2025-09-01 20:03:05.782+03	2025-09-01 20:03:05.782+03	1	2	12502	\N
37512	info@jidahmedicalcentreli.com	Information Desk	f	t	2025-09-01 20:03:05.791+03	2025-09-01 20:03:05.791+03	2	2	12502	\N
37513	P.O BOX 610-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:03:05.798+03	2025-09-01 20:03:05.798+03	14	2	12502	\N
37514	+254700000000	Facility Manager	t	t	2025-09-01 20:03:06.955+03	2025-09-01 20:03:06.955+03	1	2	12503	\N
37515	info@topcareorthopaedican.com	Information Desk	f	t	2025-09-01 20:03:06.962+03	2025-09-01 20:03:06.962+03	2	2	12503	\N
37516	P.O BOX 256-70100 GARISSA NURSING HOME Private LEVEL 3B 15GARISSA LICENCED		f	t	2025-09-01 20:03:06.97+03	2025-09-01 20:03:06.97+03	14	2	12503	\N
37517	+254700000000	Facility Manager	t	t	2025-09-01 20:03:08.486+03	2025-09-01 20:03:08.486+03	1	2	12504	\N
37518	info@annajahmedicalcareli.com	Information Desk	f	t	2025-09-01 20:03:08.494+03	2025-09-01 20:03:08.494+03	2	2	12504	\N
37519	P.O BOX 575-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 20GARISSA LICENCED		f	t	2025-09-01 20:03:08.501+03	2025-09-01 20:03:08.501+03	14	2	12504	\N
37520	+254700000000	Facility Manager	t	t	2025-09-01 20:03:08.607+03	2025-09-01 20:03:08.607+03	1	2	12505	\N
37521	info@alqudusdiagnostichos.com	Information Desk	f	t	2025-09-01 20:03:08.613+03	2025-09-01 20:03:08.613+03	2	2	12505	\N
37522	P.O BOX 374-70100 GARISSA NURSING HOME Private LEVEL 3B 20GARISSA LICENCED		f	t	2025-09-01 20:03:08.62+03	2025-09-01 20:03:08.62+03	14	2	12505	\N
37523	+254700000000	Facility Manager	t	t	2025-09-01 20:03:10.441+03	2025-09-01 20:03:10.441+03	1	2	12506	\N
37524	info@salamawellnesscentre.com	Information Desk	f	t	2025-09-01 20:03:10.448+03	2025-09-01 20:03:10.448+03	2	2	12506	\N
37525	P.O BOX 782-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 25GARISSA LICENCED		f	t	2025-09-01 20:03:10.457+03	2025-09-01 20:03:10.457+03	14	2	12506	\N
37526	+254700000000	Facility Manager	t	t	2025-09-01 20:03:11.762+03	2025-09-01 20:03:11.762+03	1	2	12507	\N
37527	info@garissauniversitycli.com	Information Desk	f	t	2025-09-01 20:03:11.77+03	2025-09-01 20:03:11.77+03	2	2	12507	\N
37528	P.O BOX 1801-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:03:11.778+03	2025-09-01 20:03:11.778+03	14	2	12507	\N
37529	+254700000000	Facility Manager	t	t	2025-09-01 20:03:13.078+03	2025-09-01 20:03:13.078+03	1	2	12508	\N
37530	info@madyannursinghomelim.com	Information Desk	f	t	2025-09-01 20:03:13.091+03	2025-09-01 20:03:13.091+03	2	2	12508	\N
37531	P.O BOX 171-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED		f	t	2025-09-01 20:03:13.099+03	2025-09-01 20:03:13.099+03	14	2	12508	\N
37532	+254700000000	Facility Manager	t	t	2025-09-01 20:03:14.228+03	2025-09-01 20:03:14.228+03	1	2	12509	\N
37533	info@almaqdismedicalcentr.com	Information Desk	f	t	2025-09-01 20:03:14.235+03	2025-09-01 20:03:14.235+03	2	2	12509	\N
37534	P.O BOX 470-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:03:14.242+03	2025-09-01 20:03:14.242+03	14	2	12509	\N
37535	+254700000000	Facility Manager	t	t	2025-09-01 20:03:15.678+03	2025-09-01 20:03:15.678+03	1	2	12510	\N
37536	info@bayaneyecarelimited.com	Information Desk	f	t	2025-09-01 20:03:15.684+03	2025-09-01 20:03:15.684+03	2	2	12510	\N
37537	P.O BOX 1520-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:03:15.69+03	2025-09-01 20:03:15.69+03	14	2	12510	\N
37538	+254700000000	Facility Manager	t	t	2025-09-01 20:03:16.827+03	2025-09-01 20:03:16.827+03	1	2	12511	\N
37539	info@alhadafmedicalclinic.com	Information Desk	f	t	2025-09-01 20:03:16.836+03	2025-09-01 20:03:16.836+03	2	2	12511	\N
37540	P.O BOX 209-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:03:16.843+03	2025-09-01 20:03:16.843+03	14	2	12511	\N
37541	+254700000000	Facility Manager	t	t	2025-09-01 20:03:18.164+03	2025-09-01 20:03:18.164+03	1	2	12512	\N
37542	info@abuuamiranursinghome.com	Information Desk	f	t	2025-09-01 20:03:18.177+03	2025-09-01 20:03:18.177+03	2	2	12512	\N
37543	P.O BOX 405-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:03:18.184+03	2025-09-01 20:03:18.184+03	14	2	12512	\N
37544	+254700000000	Facility Manager	t	t	2025-09-01 20:03:19.433+03	2025-09-01 20:03:19.433+03	1	2	12513	\N
37545	info@internationalopticac.com	Information Desk	f	t	2025-09-01 20:03:19.44+03	2025-09-01 20:03:19.44+03	2	2	12513	\N
37546	P.O BOX 86002-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:03:19.448+03	2025-09-01 20:03:19.448+03	14	2	12513	\N
37547	+254700000000	Facility Manager	t	t	2025-09-01 20:03:21.089+03	2025-09-01 20:03:21.089+03	1	2	12514	\N
37548	info@tolsanmedicalcenter.com	Information Desk	f	t	2025-09-01 20:03:21.099+03	2025-09-01 20:03:21.099+03	2	2	12514	\N
37549	P.O BOX 70100-70100 GARISSA MEDICAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:03:21.107+03	2025-09-01 20:03:21.107+03	14	2	12514	\N
37550	+254700000000	Facility Manager	t	t	2025-09-01 20:03:22.449+03	2025-09-01 20:03:22.449+03	1	2	12515	\N
37551	info@malifisahospitallimi.com	Information Desk	f	t	2025-09-01 20:03:22.457+03	2025-09-01 20:03:22.457+03	2	2	12515	\N
37552	P.O BOX 103-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 0GARISSA LICENCED		f	t	2025-09-01 20:03:22.463+03	2025-09-01 20:03:22.463+03	14	2	12515	\N
37553	+254700000000	Facility Manager	t	t	2025-09-01 20:03:23.58+03	2025-09-01 20:03:23.58+03	1	2	12516	\N
37554	info@garissaeyeandorthodo.com	Information Desk	f	t	2025-09-01 20:03:23.589+03	2025-09-01 20:03:23.589+03	2	2	12516	\N
37555	P.O BOX 1474-70100 GARISSA NURSING HOME Private LEVEL 3B 4GARISSA LICENCED		f	t	2025-09-01 20:03:23.595+03	2025-09-01 20:03:23.595+03	14	2	12516	\N
37556	+254700000000	Facility Manager	t	t	2025-09-01 20:03:25.13+03	2025-09-01 20:03:25.13+03	1	2	12517	\N
37557	info@anfalmedicalcenterli.com	Information Desk	f	t	2025-09-01 20:03:25.139+03	2025-09-01 20:03:25.139+03	2	2	12517	\N
37558	P.O BOX 514-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED		f	t	2025-09-01 20:03:25.147+03	2025-09-01 20:03:25.147+03	14	2	12517	\N
37559	+254700000000	Facility Manager	t	t	2025-09-01 20:03:26.271+03	2025-09-01 20:03:26.271+03	1	2	12518	\N
37560	info@drsmiledentalclinicl.com	Information Desk	f	t	2025-09-01 20:03:26.278+03	2025-09-01 20:03:26.278+03	2	2	12518	\N
37561	P.O BOX 254727670640-70100 GARISSA DENTAL CLINIC Private LEVEL 2 0GARISSA LICENCED		f	t	2025-09-01 20:03:26.285+03	2025-09-01 20:03:26.285+03	14	2	12518	\N
37562	+254700000000	Facility Manager	t	t	2025-09-01 20:03:27.718+03	2025-09-01 20:03:27.718+03	1	2	12519	\N
37563	info@arqammedicalcentre.com	Information Desk	f	t	2025-09-01 20:03:27.726+03	2025-09-01 20:03:27.726+03	2	2	12519	\N
37564	P.O BOX 39-70100 GARISSA MEDICAL CENTRE Private LEVEL 3A 15GARISSA LICENCED		f	t	2025-09-01 20:03:27.733+03	2025-09-01 20:03:27.733+03	14	2	12519	\N
37565	+254700000000	Facility Manager	t	t	2025-09-01 20:03:28.712+03	2025-09-01 20:03:28.712+03	1	2	12520	\N
37566	info@waberihospitalltd.com	Information Desk	f	t	2025-09-01 20:03:28.719+03	2025-09-01 20:03:28.719+03	2	2	12520	\N
37567	P.O BOX 957-70100 GARISSA NURSING HOME Private LEVEL 3B 40GARISSA LICENCED		f	t	2025-09-01 20:03:28.727+03	2025-09-01 20:03:28.727+03	14	2	12520	\N
37568	+254700000000	Facility Manager	t	t	2025-09-01 20:03:30.089+03	2025-09-01 20:03:30.089+03	1	2	12521	\N
37569	info@reussetroyermissionh.com	Information Desk	f	t	2025-09-01 20:03:30.1+03	2025-09-01 20:03:30.1+03	2	2	12521	\N
37570	P.O BOX 844-40400 MIGORI HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 6HOMA BAY LICENCED		f	t	2025-09-01 20:03:30.11+03	2025-09-01 20:03:30.11+03	14	2	12521	\N
37571	+254700000000	Facility Manager	t	t	2025-09-01 20:03:31.703+03	2025-09-01 20:03:31.703+03	1	2	12522	\N
37572	info@f.s.jst.theresaasumb.com	Information Desk	f	t	2025-09-01 20:03:31.709+03	2025-09-01 20:03:31.709+03	2	2	12522	\N
37573	P.O BOX 669-40200 KISII FAITH BASED LEVEL 4 HOSPITAL FAITH BASED ORGANIZATION (FBO) LEVEL 4 73HOMA BAY LICENCED		f	t	2025-09-01 20:03:31.715+03	2025-09-01 20:03:31.716+03	14	2	12522	\N
37574	+254700000000	Facility Manager	t	t	2025-09-01 20:03:33.343+03	2025-09-01 20:03:33.343+03	1	2	12523	\N
37575	info@sttheresafsjasumbiro.com	Information Desk	f	t	2025-09-01 20:03:33.351+03	2025-09-01 20:03:33.351+03	2	2	12523	\N
37576	P.O BOX 669-40200 KISII FAITH BASED DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:33.357+03	2025-09-01 20:03:33.357+03	14	2	12523	\N
37577	+254700000000	Facility Manager	t	t	2025-09-01 20:03:34.785+03	2025-09-01 20:03:34.785+03	1	2	12524	\N
37578	info@afyaresearchafricamf.com	Information Desk	f	t	2025-09-01 20:03:34.792+03	2025-09-01 20:03:34.792+03	2	2	12524	\N
37579	P.O BOX 20880-00202 NAIROBI HEALTH CENTRE Private LEVEL 3B 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:34.799+03	2025-09-01 20:03:34.799+03	14	2	12524	\N
37580	+254700000000	Facility Manager	t	t	2025-09-01 20:03:36.848+03	2025-09-01 20:03:36.848+03	1	2	12525	\N
37581	info@okittanursingandmate.com	Information Desk	f	t	2025-09-01 20:03:36.857+03	2025-09-01 20:03:36.857+03	2	2	12525	\N
37582	P.O BOX 4-40223 KADONGO KISUMU NURSING HOME Private LEVEL 3B 54HOMA BAY LICENCED		f	t	2025-09-01 20:03:36.864+03	2025-09-01 20:03:36.864+03	14	2	12525	\N
37583	+254700000000	Facility Manager	t	t	2025-09-01 20:03:38.388+03	2025-09-01 20:03:38.388+03	1	2	12526	\N
37584	info@portflorencecommunit.com	Information Desk	f	t	2025-09-01 20:03:38.395+03	2025-09-01 20:03:38.395+03	2	2	12526	\N
37585	P.O BOX 3417-40100 KISUMU MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:38.401+03	2025-09-01 20:03:38.401+03	14	2	12526	\N
37586	+254700000000	Facility Manager	t	t	2025-09-01 20:03:38.491+03	2025-09-01 20:03:38.491+03	1	2	12527	\N
37587	info@theagakhanhospitalho.com	Information Desk	f	t	2025-09-01 20:03:38.497+03	2025-09-01 20:03:38.497+03	2	2	12527	\N
37588	P.O BOX 530-40100 KISUMU MEDICAL CENTRE Private LEVEL 3A 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:38.504+03	2025-09-01 20:03:38.504+03	14	2	12527	\N
37589	+254700000000	Facility Manager	t	t	2025-09-01 20:03:39.843+03	2025-09-01 20:03:39.843+03	1	2	12528	\N
37590	info@wattamedicalclinic.com	Information Desk	f	t	2025-09-01 20:03:39.851+03	2025-09-01 20:03:39.851+03	2	2	12528	\N
37591	P.O BOX 36-40400 SUNA - MIGORI MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:39.858+03	2025-09-01 20:03:39.858+03	14	2	12528	\N
37592	+254700000000	Facility Manager	t	t	2025-09-01 20:03:41.538+03	2025-09-01 20:03:41.538+03	1	2	12529	\N
37593	info@portflorencecommunit.com	Information Desk	f	t	2025-09-01 20:03:41.56+03	2025-09-01 20:03:41.56+03	2	2	12529	\N
37594	P.O BOX 3417-40100 KISUMU NURSING HOME Private LEVEL 3B 35HOMA BAY LICENCED		f	t	2025-09-01 20:03:41.586+03	2025-09-01 20:03:41.586+03	14	2	12529	\N
37595	+254700000000	Facility Manager	t	t	2025-09-01 20:03:43.427+03	2025-09-01 20:03:43.427+03	1	2	12530	\N
37596	info@katitomedicalcentrem.com	Information Desk	f	t	2025-09-01 20:03:43.434+03	2025-09-01 20:03:43.434+03	2	2	12530	\N
37597	P.O BOX 1764-40100 KISUMU HOSPITAL LEVEL 4 Private LEVEL 4 75HOMA BAY LICENCED		f	t	2025-09-01 20:03:43.441+03	2025-09-01 20:03:43.441+03	14	2	12530	\N
37598	+254700000000	Facility Manager	t	t	2025-09-01 20:03:44.765+03	2025-09-01 20:03:44.765+03	1	2	12531	\N
37599	info@blisshealthcareltdho.com	Information Desk	f	t	2025-09-01 20:03:44.772+03	2025-09-01 20:03:44.772+03	2	2	12531	\N
37600	P.O BOX 5763-00200 NAIROBI MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:44.78+03	2025-09-01 20:03:44.78+03	14	2	12531	\N
37601	+254700000000	Facility Manager	t	t	2025-09-01 20:03:46.326+03	2025-09-01 20:03:46.326+03	1	2	12532	\N
37602	info@tudorhealthcareltdsi.com	Information Desk	f	t	2025-09-01 20:03:46.334+03	2025-09-01 20:03:46.334+03	2	2	12532	\N
37603	P.O BOX 91291-80100 MOMBASA NURSING HOME Private LEVEL 3B 35HOMA BAY LICENCED		f	t	2025-09-01 20:03:46.341+03	2025-09-01 20:03:46.342+03	14	2	12532	\N
37604	+254700000000	Facility Manager	t	t	2025-09-01 20:03:47.87+03	2025-09-01 20:03:47.87+03	1	2	12533	\N
37605	info@hawifamilyhospital.com	Information Desk	f	t	2025-09-01 20:03:47.877+03	2025-09-01 20:03:47.877+03	2	2	12533	\N
37606	P.O BOX 1251-40100 KISUMU HOSPITAL LEVEL 4 Private LEVEL 4 120 HOMA BAY LICENCED		f	t	2025-09-01 20:03:47.883+03	2025-09-01 20:03:47.883+03	14	2	12533	\N
37607	+254700000000	Facility Manager	t	t	2025-09-01 20:03:49.648+03	2025-09-01 20:03:49.648+03	1	2	12534	\N
37608	info@manyattacommunitynur.com	Information Desk	f	t	2025-09-01 20:03:49.667+03	2025-09-01 20:03:49.67+03	2	2	12534	\N
37609	P.O BOX 1896-40100 KISUMU NURSING HOME Private LEVEL 3B 34HOMA BAY LICENCED		f	t	2025-09-01 20:03:49.684+03	2025-09-01 20:03:49.684+03	14	2	12534	\N
37610	+254700000000	Facility Manager	t	t	2025-09-01 20:03:51.163+03	2025-09-01 20:03:51.163+03	1	2	12535	\N
37611	info@nguonomedicalcentre.com	Information Desk	f	t	2025-09-01 20:03:51.17+03	2025-09-01 20:03:51.17+03	2	2	12535	\N
37612	P.O BOX 2155-40100 KISUMU MEDICAL CENTRE Private LEVEL 3A 40HOMA BAY LICENCED		f	t	2025-09-01 20:03:51.179+03	2025-09-01 20:03:51.179+03	14	2	12535	\N
37613	+254700000000	Facility Manager	t	t	2025-09-01 20:03:52.3+03	2025-09-01 20:03:52.3+03	1	2	12536	\N
37614	info@jatrizmedicalcentre.com	Information Desk	f	t	2025-09-01 20:03:52.306+03	2025-09-01 20:03:52.306+03	2	2	12536	\N
37615	P.O BOX 745-50200 BUNGOMA MEDICAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:52.316+03	2025-09-01 20:03:52.316+03	14	2	12536	\N
37616	+254700000000	Facility Manager	t	t	2025-09-01 20:03:53.471+03	2025-09-01 20:03:53.471+03	1	2	12537	\N
37617	info@flodentalclinic.com	Information Desk	f	t	2025-09-01 20:03:53.481+03	2025-09-01 20:03:53.481+03	2	2	12537	\N
37618	P.O BOX 1236-40100 KISUMU DENTAL CLINIC Private LEVEL 2 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:53.488+03	2025-09-01 20:03:53.488+03	14	2	12537	\N
37619	+254700000000	Facility Manager	t	t	2025-09-01 20:03:54.834+03	2025-09-01 20:03:54.834+03	1	2	12538	\N
37620	info@rakshainternationalm.com	Information Desk	f	t	2025-09-01 20:03:54.857+03	2025-09-01 20:03:54.857+03	2	2	12538	\N
37621	P.O BOX 8452-00200 NAIROBI HOSPITAL LEVEL 4 Private LEVEL 4 76HOMA BAY LICENCED		f	t	2025-09-01 20:03:54.879+03	2025-09-01 20:03:54.879+03	14	2	12538	\N
37622	+254700000000	Facility Manager	t	t	2025-09-01 20:03:56.65+03	2025-09-01 20:03:56.65+03	1	2	12539	\N
37623	info@equityafiahomabaymed.com	Information Desk	f	t	2025-09-01 20:03:56.669+03	2025-09-01 20:03:56.669+03	2	2	12539	\N
37624	P.O BOX 41693-00100 NAIROBI MEDICAL CENTRE Private LEVEL 3A 0HOMA BAY LICENCED		f	t	2025-09-01 20:03:56.69+03	2025-09-01 20:03:56.69+03	14	2	12539	\N
37625	+254700000000	Facility Manager	t	t	2025-09-01 20:03:58.381+03	2025-09-01 20:03:58.381+03	1	2	12540	\N
37626	info@rehemahospiceandclin.com	Information Desk	f	t	2025-09-01 20:03:58.389+03	2025-09-01 20:03:58.389+03	2	2	12540	\N
37627	P.O BOX 3072-40100 KISUMU NURSING HOME Private LEVEL 3B 19HOMA BAY LICENCED		f	t	2025-09-01 20:03:58.396+03	2025-09-01 20:03:58.396+03	14	2	12540	\N
37628	+254700000000	Facility Manager	t	t	2025-09-01 20:04:00.426+03	2025-09-01 20:04:00.426+03	1	2	12541	\N
37629	info@perisquremedicalclin.com	Information Desk	f	t	2025-09-01 20:04:00.445+03	2025-09-01 20:04:00.445+03	2	2	12541	\N
37630	P.O BOX 997-00100 NAIROBI MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:00.471+03	2025-09-01 20:04:00.471+03	14	2	12541	\N
37631	+254700000000	Facility Manager	t	t	2025-09-01 20:04:02.716+03	2025-09-01 20:04:02.716+03	1	2	12542	\N
37632	info@isioloregionalhospit.com	Information Desk	f	t	2025-09-01 20:04:02.728+03	2025-09-01 20:04:02.728+03	2	2	12542	\N
37633	P.O BOX 66- ISIOLO HOSPITAL LEVEL 4 Public LEVEL 4 80ISIOLO LICENCED		f	t	2025-09-01 20:04:02.738+03	2025-09-01 20:04:02.738+03	14	2	12542	\N
37634	+254700000000	Facility Manager	t	t	2025-09-01 20:04:04.841+03	2025-09-01 20:04:04.841+03	1	2	12543	\N
37635	info@aicisiolodispensary.com	Information Desk	f	t	2025-09-01 20:04:04.852+03	2025-09-01 20:04:04.852+03	2	2	12543	\N
37636	P.O BOX 262-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:04.866+03	2025-09-01 20:04:04.866+03	14	2	12543	\N
37637	+254700000000	Facility Manager	t	t	2025-09-01 20:04:05.118+03	2025-09-01 20:04:05.118+03	1	2	12544	\N
37638	info@a.c.kisiolodispensar.com	Information Desk	f	t	2025-09-01 20:04:05.128+03	2025-09-01 20:04:05.128+03	2	2	12544	\N
37639	P.O BOX 110-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:05.14+03	2025-09-01 20:04:05.14+03	14	2	12544	\N
37640	+254700000000	Facility Manager	t	t	2025-09-01 20:04:05.393+03	2025-09-01 20:04:05.393+03	1	2	12545	\N
37641	info@archerspostcatholich.com	Information Desk	f	t	2025-09-01 20:04:05.408+03	2025-09-01 20:04:05.408+03	2	2	12545	\N
37642	P.O BOX 359-60300 ISIOLO FAITH-BASED BASIC CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3A 31ISIOLO LICENCED		f	t	2025-09-01 20:04:05.421+03	2025-09-01 20:04:05.421+03	14	2	12545	\N
37643	+254700000000	Facility Manager	t	t	2025-09-01 20:04:07.36+03	2025-09-01 20:04:07.36+03	1	2	12546	\N
37644	info@isiolocatholicdispen.com	Information Desk	f	t	2025-09-01 20:04:07.369+03	2025-09-01 20:04:07.369+03	2	2	12546	\N
37645	P.O BOX 162-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:07.382+03	2025-09-01 20:04:07.382+03	14	2	12546	\N
37646	+254700000000	Facility Manager	t	t	2025-09-01 20:04:08.801+03	2025-09-01 20:04:08.801+03	1	2	12547	\N
37647	info@st.johnpauliiavimate.com	Information Desk	f	t	2025-09-01 20:04:08.81+03	2025-09-01 20:04:08.81+03	2	2	12547	\N
37648	P.O BOX 340-60300 ISIOLO HEALTH CENTRE FAITH BASED ORGANIZATION (FBO) LEVEL 3B 40ISIOLO LICENCED		f	t	2025-09-01 20:04:08.819+03	2025-09-01 20:04:08.819+03	14	2	12547	\N
37649	+254700000000	Facility Manager	t	t	2025-09-01 20:04:10.555+03	2025-09-01 20:04:10.555+03	1	2	12548	\N
37650	info@campgarbacatholicdis.com	Information Desk	f	t	2025-09-01 20:04:10.563+03	2025-09-01 20:04:10.563+03	2	2	12548	\N
37651	P.O BOX 319-60300 ISIOLO DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:10.572+03	2025-09-01 20:04:10.572+03	14	2	12548	\N
37652	+254700000000	Facility Manager	t	t	2025-09-01 20:04:12.296+03	2025-09-01 20:04:12.296+03	1	2	12549	\N
37653	info@catholicdispensaryng.com	Information Desk	f	t	2025-09-01 20:04:12.305+03	2025-09-01 20:04:12.305+03	2	2	12549	\N
37654	P.O BOX 232-60300 ISIOLO FAITH BASED DISPENSARY FAITH BASED ORGANIZATION (FBO) LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:12.315+03	2025-09-01 20:04:12.315+03	14	2	12549	\N
37655	+254700000000	Facility Manager	t	t	2025-09-01 20:04:14.155+03	2025-09-01 20:04:14.155+03	1	2	12550	\N
37656	info@leparuacommunitymedi.com	Information Desk	f	t	2025-09-01 20:04:14.173+03	2025-09-01 20:04:14.173+03	2	2	12550	\N
37657	P.O BOX PRIV ATE BAG-60300 ISIOLO MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:14.183+03	2025-09-01 20:04:14.183+03	14	2	12550	\N
37658	+254700000000	Facility Manager	t	t	2025-09-01 20:04:16.315+03	2025-09-01 20:04:16.315+03	1	2	12551	\N
37659	info@pepolatumainijangwan.com	Information Desk	f	t	2025-09-01 20:04:16.324+03	2025-09-01 20:04:16.324+03	2	2	12551	\N
37660	P.O BOX 280-60300 ISIOLO MEDICAL CENTRE Private LEVEL 3A 0ISIOLO LICENCED		f	t	2025-09-01 20:04:16.335+03	2025-09-01 20:04:16.335+03	14	2	12551	\N
37661	+254700000000	Facility Manager	t	t	2025-09-01 20:04:18.37+03	2025-09-01 20:04:18.37+03	1	2	12552	\N
37662	info@iqramedicalcentreand.com	Information Desk	f	t	2025-09-01 20:04:18.384+03	2025-09-01 20:04:18.384+03	2	2	12552	\N
37663	P.O BOX 131-60300 ISIOLO NURSING HOME Private LEVEL 3B 40ISIOLO LICENCED		f	t	2025-09-01 20:04:18.392+03	2025-09-01 20:04:18.392+03	14	2	12552	\N
37664	+254700000000	Facility Manager	t	t	2025-09-01 20:04:18.506+03	2025-09-01 20:04:18.506+03	1	2	12553	\N
37665	info@isiolocountynursingh.com	Information Desk	f	t	2025-09-01 20:04:18.512+03	2025-09-01 20:04:18.512+03	2	2	12553	\N
37666	P.O BOX 588- ISIOLO NURSING HOME Private LEVEL 3B 20ISIOLO LICENCED		f	t	2025-09-01 20:04:18.519+03	2025-09-01 20:04:18.519+03	14	2	12553	\N
37667	+254700000000	Facility Manager	t	t	2025-09-01 20:04:19.754+03	2025-09-01 20:04:19.754+03	1	2	12554	\N
37668	info@kulamawemedicalservi.com	Information Desk	f	t	2025-09-01 20:04:19.763+03	2025-09-01 20:04:19.763+03	2	2	12554	\N
37669	P.O BOX 670-60300 ISIOLO MEDICAL CENTRE Private LEVEL 3A 12ISIOLO LICENCED		f	t	2025-09-01 20:04:19.77+03	2025-09-01 20:04:19.77+03	14	2	12554	\N
37670	+254700000000	Facility Manager	t	t	2025-09-01 20:04:21.573+03	2025-09-01 20:04:21.573+03	1	2	12555	\N
37671	info@downtownmedicalclini.com	Information Desk	f	t	2025-09-01 20:04:21.58+03	2025-09-01 20:04:21.58+03	2	2	12555	\N
37672	P.O BOX 247-60300 ISIOLO MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:21.594+03	2025-09-01 20:04:21.594+03	14	2	12555	\N
37673	+254700000000	Facility Manager	t	t	2025-09-01 20:04:23.088+03	2025-09-01 20:04:23.088+03	1	2	12556	\N
37674	info@healthpacthospital.com	Information Desk	f	t	2025-09-01 20:04:23.095+03	2025-09-01 20:04:23.095+03	2	2	12556	\N
37675	P.O BOX 457-60300 ISIOLO HOSPITAL LEVEL 4 Private LEVEL 4 30ISIOLO LICENCED		f	t	2025-09-01 20:04:23.103+03	2025-09-01 20:04:23.103+03	14	2	12556	\N
37676	+254700000000	Facility Manager	t	t	2025-09-01 20:04:24.351+03	2025-09-01 20:04:24.351+03	1	2	12557	\N
37677	info@simbaclinic.com	Information Desk	f	t	2025-09-01 20:04:24.358+03	2025-09-01 20:04:24.358+03	2	2	12557	\N
37678	P.O BOX 782-60300 ISIOLO MEDICAL CLINIC Private LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:24.365+03	2025-09-01 20:04:24.365+03	14	2	12557	\N
37679	+254700000000	Facility Manager	t	t	2025-09-01 20:04:24.474+03	2025-09-01 20:04:24.474+03	1	2	12558	\N
37680	info@wasoaipcadispensary.com	Information Desk	f	t	2025-09-01 20:04:24.48+03	2025-09-01 20:04:24.48+03	2	2	12558	\N
37681	P.O BOX 727- ISIOLO DISPENSARY Private LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:24.486+03	2025-09-01 20:04:24.486+03	14	2	12558	\N
37682	+254700000000	Facility Manager	t	t	2025-09-01 20:04:26.142+03	2025-09-01 20:04:26.142+03	1	2	12559	\N
37683	info@almasmedicalservices.com	Information Desk	f	t	2025-09-01 20:04:26.153+03	2025-09-01 20:04:26.153+03	2	2	12559	\N
37684	P.O BOX 652-60300 ISIOLO NURSING HOME Private LEVEL 3B 18ISIOLO LICENCED		f	t	2025-09-01 20:04:26.168+03	2025-09-01 20:04:26.168+03	14	2	12559	\N
37685	+254700000000	Facility Manager	t	t	2025-09-01 20:04:27.802+03	2025-09-01 20:04:27.802+03	1	2	12560	\N
37686	info@elephantdentalisiolo.com	Information Desk	f	t	2025-09-01 20:04:27.81+03	2025-09-01 20:04:27.81+03	2	2	12560	\N
37687	P.O BOX 821-60300 ISIOLO DENTAL CLINIC Private LEVEL 2 0ISIOLO LICENCED		f	t	2025-09-01 20:04:27.817+03	2025-09-01 20:04:27.817+03	14	2	12560	\N
37688	+254700000000	Facility Manager	t	t	2025-09-01 20:04:29.302+03	2025-09-01 20:04:29.302+03	1	2	12561	\N
37689	info@galaxyhospitallimite.com	Information Desk	f	t	2025-09-01 20:04:29.308+03	2025-09-01 20:04:29.308+03	2	2	12561	\N
37690	P.O BOX 674-60300 ISIOLO Hospital Level 5 Private LEVEL 5 70ISIOLO LICENCED		f	t	2025-09-01 20:04:29.315+03	2025-09-01 20:04:29.315+03	14	2	12561	\N
\.


--
-- TOC entry 4104 (class 0 OID 67416)
-- Dependencies: 277
-- Data for Name: facility_coordinates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facility_coordinates (coordinate_id, latitude, longitude, collection_date, data_source, collection_method, created_at, updated_at, facility_id) FROM stdin;
12203	0.46670000	35.96670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:35.225+03	2025-09-01 19:56:35.225+03	12201
12204	0.46670000	35.96670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:37.305+03	2025-09-01 19:56:37.305+03	12202
12205	-1.28240000	36.75028000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:37.392+03	2025-09-01 19:56:37.392+03	12203
12206	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:39.016+03	2025-09-01 19:56:39.016+03	12204
12207	0.58493800	34.48262100	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:39.075+03	2025-09-01 19:56:39.075+03	12205
12208	-0.04476000	36.21677000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:40.422+03	2025-09-01 19:56:40.422+03	12206
12209	0.49896000	34.45451000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:40.514+03	2025-09-01 19:56:40.514+03	12207
12210	0.57568000	34.55689000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:40.601+03	2025-09-01 19:56:40.601+03	12208
12211	0.47438000	34.52570000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:40.656+03	2025-09-01 19:56:40.656+03	12209
12212	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:41.847+03	2025-09-01 19:56:41.847+03	12210
12213	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:43.353+03	2025-09-01 19:56:43.353+03	12211
12214	0.66925500	34.52810000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:43.413+03	2025-09-01 19:56:43.413+03	12212
12215	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:44.694+03	2025-09-01 19:56:44.694+03	12213
12216	0.57548000	34.55943000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:46.287+03	2025-09-01 19:56:46.287+03	12214
12217	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:47.704+03	2025-09-01 19:56:47.704+03	12215
12218	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:49.366+03	2025-09-01 19:56:49.366+03	12216
12219	0.60372000	34.40690000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:49.437+03	2025-09-01 19:56:49.437+03	12217
12220	0.50208000	34.65840000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:49.504+03	2025-09-01 19:56:49.504+03	12218
12221	0.61193900	34.65829200	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:49.567+03	2025-09-01 19:56:49.568+03	12219
12222	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:50.703+03	2025-09-01 19:56:50.703+03	12220
12223	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:51.99+03	2025-09-01 19:56:51.99+03	12221
12224	0.49746000	34.48410000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:56:52.052+03	2025-09-01 19:56:52.052+03	12222
12225	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:53.297+03	2025-09-01 19:56:53.297+03	12223
12226	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:54.989+03	2025-09-01 19:56:54.989+03	12224
12227	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:56.196+03	2025-09-01 19:56:56.196+03	12225
12228	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:57.427+03	2025-09-01 19:56:57.427+03	12226
12229	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:58.683+03	2025-09-01 19:56:58.683+03	12227
12230	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:56:59.766+03	2025-09-01 19:56:59.766+03	12228
12231	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:01.289+03	2025-09-01 19:57:01.289+03	12229
12232	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:02.563+03	2025-09-01 19:57:02.563+03	12230
12233	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:04.298+03	2025-09-01 19:57:04.298+03	12231
12234	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:05.928+03	2025-09-01 19:57:05.928+03	12232
12235	-1.22089000	36.89408000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:07.835+03	2025-09-01 19:57:07.835+03	12233
12236	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:09.042+03	2025-09-01 19:57:09.042+03	12234
12237	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:10.509+03	2025-09-01 19:57:10.509+03	12235
12238	0.57691600	34.55349000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:10.581+03	2025-09-01 19:57:10.581+03	12236
12239	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:12.185+03	2025-09-01 19:57:12.185+03	12237
12240	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:13.724+03	2025-09-01 19:57:13.724+03	12238
12241	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:15.246+03	2025-09-01 19:57:15.246+03	12239
12242	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:16.708+03	2025-09-01 19:57:16.708+03	12240
12243	0.56893000	34.56295000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:18.837+03	2025-09-01 19:57:18.837+03	12241
12244	0.76134000	34.54924000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:20.534+03	2025-09-01 19:57:20.534+03	12242
12245	0.57167000	34.65132000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:20.61+03	2025-09-01 19:57:20.61+03	12243
12246	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:22.018+03	2025-09-01 19:57:22.018+03	12244
12247	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:23.725+03	2025-09-01 19:57:23.725+03	12245
12248	0.55665000	34.55993000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:23.791+03	2025-09-01 19:57:23.791+03	12246
12249	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:25.127+03	2025-09-01 19:57:25.127+03	12247
12250	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:26.429+03	2025-09-01 19:57:26.429+03	12248
12251	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:28.119+03	2025-09-01 19:57:28.119+03	12249
12252	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:29.698+03	2025-09-01 19:57:29.698+03	12250
12253	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:31.146+03	2025-09-01 19:57:31.146+03	12251
12254	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:32.535+03	2025-09-01 19:57:32.535+03	12252
12255	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:33.603+03	2025-09-01 19:57:33.603+03	12253
12256	0.50927000	35.28773000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:35.15+03	2025-09-01 19:57:35.15+03	12254
12257	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:36.129+03	2025-09-01 19:57:36.129+03	12255
12258	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:37.826+03	2025-09-01 19:57:37.826+03	12256
12259	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:39.174+03	2025-09-01 19:57:39.174+03	12257
12260	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:40.866+03	2025-09-01 19:57:40.866+03	12258
12261	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:43.027+03	2025-09-01 19:57:43.027+03	12259
12262	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:44.591+03	2025-09-01 19:57:44.591+03	12260
12263	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:46.073+03	2025-09-01 19:57:46.073+03	12261
12264	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:47.674+03	2025-09-01 19:57:47.674+03	12262
12265	0.28330000	34.75000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:50.524+03	2025-09-01 19:57:50.524+03	12263
12266	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:52.39+03	2025-09-01 19:57:52.39+03	12264
12267	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:54.161+03	2025-09-01 19:57:54.161+03	12265
12268	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:55.495+03	2025-09-01 19:57:55.495+03	12266
12269	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:57:57.199+03	2025-09-01 19:57:57.199+03	12267
12270	-0.87247100	34.19671100	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:57:58.398+03	2025-09-01 19:57:58.398+03	12268
12271	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:00.528+03	2025-09-01 19:58:00.528+03	12269
12272	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:02.317+03	2025-09-01 19:58:02.317+03	12270
12273	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:03.975+03	2025-09-01 19:58:03.975+03	12271
12274	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:05.832+03	2025-09-01 19:58:05.832+03	12272
12275	-1.06437000	34.47373000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:07.584+03	2025-09-01 19:58:07.584+03	12273
12276	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:09.139+03	2025-09-01 19:58:09.139+03	12274
12277	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:10.79+03	2025-09-01 19:58:10.79+03	12275
12278	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:12.71+03	2025-09-01 19:58:12.71+03	12276
12279	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:14.037+03	2025-09-01 19:58:14.037+03	12277
12280	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:15.713+03	2025-09-01 19:58:15.713+03	12278
12281	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:17.335+03	2025-09-01 19:58:17.335+03	12279
12282	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:19.041+03	2025-09-01 19:58:19.041+03	12280
12283	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:20.348+03	2025-09-01 19:58:20.348+03	12281
12284	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:22.165+03	2025-09-01 19:58:22.165+03	12282
12285	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:23.861+03	2025-09-01 19:58:23.861+03	12283
12286	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:25.621+03	2025-09-01 19:58:25.621+03	12284
12287	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:27.265+03	2025-09-01 19:58:27.265+03	12285
12288	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:29.076+03	2025-09-01 19:58:29.076+03	12286
12289	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:30.592+03	2025-09-01 19:58:30.592+03	12287
12290	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:32.324+03	2025-09-01 19:58:32.324+03	12288
12291	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:33.648+03	2025-09-01 19:58:33.648+03	12289
12292	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:34.767+03	2025-09-01 19:58:34.767+03	12290
12293	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:36.164+03	2025-09-01 19:58:36.164+03	12291
12294	0.90143000	34.94941000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:37.681+03	2025-09-01 19:58:37.681+03	12292
12295	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:38.804+03	2025-09-01 19:58:38.804+03	12293
12296	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:40.281+03	2025-09-01 19:58:40.281+03	12294
12297	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:41.749+03	2025-09-01 19:58:41.749+03	12295
12298	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:43.566+03	2025-09-01 19:58:43.566+03	12296
12299	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:45.03+03	2025-09-01 19:58:45.03+03	12297
12300	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:46.348+03	2025-09-01 19:58:46.348+03	12298
12301	0.27749000	34.10545000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:46.432+03	2025-09-01 19:58:46.432+03	12299
12302	0.30425000	34.10295000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:47.806+03	2025-09-01 19:58:47.806+03	12300
12303	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:49.206+03	2025-09-01 19:58:49.206+03	12301
12304	0.45378600	34.11800000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:49.291+03	2025-09-01 19:58:49.291+03	12302
12305	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:50.731+03	2025-09-01 19:58:50.731+03	12303
12306	0.30464000	34.20157000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:50.805+03	2025-09-01 19:58:50.805+03	12304
12307	0.27844000	34.11799000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:50.888+03	2025-09-01 19:58:50.888+03	12305
12308	0.45704000	34.12430000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:58:50.951+03	2025-09-01 19:58:50.951+03	12306
12309	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:52.266+03	2025-09-01 19:58:52.266+03	12307
12310	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:53.762+03	2025-09-01 19:58:53.762+03	12308
12311	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:55.585+03	2025-09-01 19:58:55.585+03	12309
12312	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:57.732+03	2025-09-01 19:58:57.732+03	12310
12313	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:58:59.61+03	2025-09-01 19:58:59.61+03	12311
12314	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:01.538+03	2025-09-01 19:59:01.538+03	12312
12315	0.28330000	34.75000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:03.364+03	2025-09-01 19:59:03.364+03	12313
12316	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:04.786+03	2025-09-01 19:59:04.786+03	12314
12317	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:06.349+03	2025-09-01 19:59:06.349+03	12315
12318	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:07.762+03	2025-09-01 19:59:07.762+03	12316
12319	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:09.573+03	2025-09-01 19:59:09.573+03	12317
12320	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:10.987+03	2025-09-01 19:59:10.987+03	12318
12321	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:12.296+03	2025-09-01 19:59:12.296+03	12319
12322	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:13.595+03	2025-09-01 19:59:13.595+03	12320
12323	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:15.176+03	2025-09-01 19:59:15.176+03	12321
12324	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:16.408+03	2025-09-01 19:59:16.408+03	12322
12325	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:17.909+03	2025-09-01 19:59:17.909+03	12323
12326	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:19.578+03	2025-09-01 19:59:19.578+03	12324
12327	0.06670000	34.28330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:21.146+03	2025-09-01 19:59:21.146+03	12325
12328	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:22.402+03	2025-09-01 19:59:22.402+03	12326
12329	0.28330000	34.75000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:23.895+03	2025-09-01 19:59:23.895+03	12327
12330	-1.28790000	36.88149000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:59:25.186+03	2025-09-01 19:59:25.186+03	12328
12331	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:26.466+03	2025-09-01 19:59:26.466+03	12329
12332	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:28.256+03	2025-09-01 19:59:28.256+03	12330
12333	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:29.545+03	2025-09-01 19:59:29.545+03	12331
12334	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:31.213+03	2025-09-01 19:59:31.213+03	12332
12335	-1.06437000	34.47373000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:59:32.927+03	2025-09-01 19:59:32.927+03	12333
12336	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:34.311+03	2025-09-01 19:59:34.311+03	12334
12337	0.28330000	34.75000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:35.658+03	2025-09-01 19:59:35.658+03	12335
12338	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:36.975+03	2025-09-01 19:59:36.975+03	12336
12339	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:38.566+03	2025-09-01 19:59:38.566+03	12337
12340	0.46670000	34.11670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:40.047+03	2025-09-01 19:59:40.047+03	12338
12341	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:41.331+03	2025-09-01 19:59:41.331+03	12339
12342	1.73769000	40.05375000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:59:42.811+03	2025-09-01 19:59:42.811+03	12340
12343	0.52489000	35.50735000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:59:42.897+03	2025-09-01 19:59:42.897+03	12341
12344	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:44.411+03	2025-09-01 19:59:44.411+03	12342
12345	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:45.786+03	2025-09-01 19:59:45.786+03	12343
12346	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:47.119+03	2025-09-01 19:59:47.119+03	12344
12347	-0.58486000	34.39193000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:59:48.241+03	2025-09-01 19:59:48.241+03	12345
12348	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:49.714+03	2025-09-01 19:59:49.714+03	12346
12349	0.52040000	35.26990000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:51.335+03	2025-09-01 19:59:51.335+03	12347
12350	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:52.77+03	2025-09-01 19:59:52.77+03	12348
12351	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:54.166+03	2025-09-01 19:59:54.166+03	12349
12352	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:55.709+03	2025-09-01 19:59:55.709+03	12350
12353	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:56.944+03	2025-09-01 19:59:56.944+03	12351
12354	-0.43995000	37.53019000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 19:59:57.028+03	2025-09-01 19:59:57.028+03	12352
12355	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 19:59:58.379+03	2025-09-01 19:59:58.379+03	12353
12356	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:00.158+03	2025-09-01 20:00:00.158+03	12354
12357	-0.41331000	37.58781000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:00.249+03	2025-09-01 20:00:00.249+03	12355
12358	-0.53518000	37.47850000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:01.902+03	2025-09-01 20:00:01.902+03	12356
12359	-0.65624000	37.56268000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:02.09+03	2025-09-01 20:00:02.09+03	12357
12360	-0.43103000	37.44415000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:02.204+03	2025-09-01 20:00:02.204+03	12358
12361	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:03.409+03	2025-09-01 20:00:03.409+03	12359
12362	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:04.725+03	2025-09-01 20:00:04.725+03	12360
12363	-0.43859000	37.53214000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:04.81+03	2025-09-01 20:00:04.81+03	12361
12364	-0.55287000	37.47047000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:04.889+03	2025-09-01 20:00:04.889+03	12362
12365	-0.52903000	37.45801000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:04.968+03	2025-09-01 20:00:04.968+03	12363
12366	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:06.196+03	2025-09-01 20:00:06.196+03	12364
12367	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:07.856+03	2025-09-01 20:00:07.856+03	12365
12368	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:09.139+03	2025-09-01 20:00:09.139+03	12366
12369	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:10.44+03	2025-09-01 20:00:10.44+03	12367
12370	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:11.856+03	2025-09-01 20:00:11.856+03	12368
12371	-0.68873000	37.36255000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:11.94+03	2025-09-01 20:00:11.94+03	12369
12372	-0.54698000	37.45436000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:12.029+03	2025-09-01 20:00:12.029+03	12370
12373	-0.54218000	37.46597000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:13.474+03	2025-09-01 20:00:13.474+03	12371
12374	-0.54496000	37.45496000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:13.561+03	2025-09-01 20:00:13.561+03	12372
12375	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:14.79+03	2025-09-01 20:00:14.79+03	12373
12376	-0.38943000	37.46371000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:15.988+03	2025-09-01 20:00:15.988+03	12374
12377	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:17.249+03	2025-09-01 20:00:17.249+03	12375
12378	-0.53674000	37.45170000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:17.35+03	2025-09-01 20:00:17.35+03	12376
12379	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:18.713+03	2025-09-01 20:00:18.713+03	12377
12380	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:19.881+03	2025-09-01 20:00:19.881+03	12378
12381	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:21.496+03	2025-09-01 20:00:21.496+03	12379
12382	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:22.941+03	2025-09-01 20:00:22.941+03	12380
12383	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:24.288+03	2025-09-01 20:00:24.288+03	12381
12384	0.05000000	37.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:25.642+03	2025-09-01 20:00:25.642+03	12382
12385	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:27.034+03	2025-09-01 20:00:27.034+03	12383
12386	-0.50480000	37.28039000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:27.151+03	2025-09-01 20:00:27.151+03	12384
12387	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:28.487+03	2025-09-01 20:00:28.487+03	12385
12388	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:29.717+03	2025-09-01 20:00:29.717+03	12386
12389	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:30.905+03	2025-09-01 20:00:30.905+03	12387
12390	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:32.397+03	2025-09-01 20:00:32.397+03	12388
12391	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:33.747+03	2025-09-01 20:00:33.747+03	12389
12392	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:35.406+03	2025-09-01 20:00:35.406+03	12390
12393	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:36.938+03	2025-09-01 20:00:36.938+03	12391
12394	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:38.141+03	2025-09-01 20:00:38.141+03	12392
12395	-4.08103000	38.86490000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:39.479+03	2025-09-01 20:00:39.479+03	12393
12396	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:41.037+03	2025-09-01 20:00:41.037+03	12394
12397	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:42.524+03	2025-09-01 20:00:42.524+03	12395
12398	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:43.878+03	2025-09-01 20:00:43.878+03	12396
12399	-0.73374000	34.84601000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:45.162+03	2025-09-01 20:00:45.162+03	12397
12400	-1.32023000	36.88918000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:45.277+03	2025-09-01 20:00:45.277+03	12398
12401	0.05000000	37.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:46.462+03	2025-09-01 20:00:46.462+03	12399
12402	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:48.481+03	2025-09-01 20:00:48.481+03	12400
12403	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:50.368+03	2025-09-01 20:00:50.368+03	12401
12404	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:52.032+03	2025-09-01 20:00:52.032+03	12402
12405	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:53.473+03	2025-09-01 20:00:53.473+03	12403
12406	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:55.39+03	2025-09-01 20:00:55.39+03	12404
12407	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:56.708+03	2025-09-01 20:00:56.708+03	12405
12408	-0.51200000	37.51984000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:56.826+03	2025-09-01 20:00:56.826+03	12406
12409	-1.14445000	36.66193000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:00:56.94+03	2025-09-01 20:00:56.94+03	12407
12410	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:00:59.064+03	2025-09-01 20:00:59.064+03	12408
12411	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:00.788+03	2025-09-01 20:01:00.788+03	12409
12412	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:02.459+03	2025-09-01 20:01:02.459+03	12410
12413	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:03.985+03	2025-09-01 20:01:03.985+03	12411
12414	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:05.504+03	2025-09-01 20:01:05.504+03	12412
12415	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:07.312+03	2025-09-01 20:01:07.312+03	12413
12416	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:08.739+03	2025-09-01 20:01:08.739+03	12414
12417	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:10.11+03	2025-09-01 20:01:10.11+03	12415
12418	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:12.206+03	2025-09-01 20:01:12.206+03	12416
12419	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:13.895+03	2025-09-01 20:01:13.895+03	12417
12420	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:15.15+03	2025-09-01 20:01:15.15+03	12418
12421	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:17.182+03	2025-09-01 20:01:17.182+03	12419
12422	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:18.718+03	2025-09-01 20:01:18.718+03	12420
12423	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:20.516+03	2025-09-01 20:01:20.516+03	12421
12424	-3.87227000	39.79793000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:01:21.949+03	2025-09-01 20:01:21.949+03	12422
12425	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:23.565+03	2025-09-01 20:01:23.565+03	12423
12426	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:24.773+03	2025-09-01 20:01:24.773+03	12424
12427	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:26.648+03	2025-09-01 20:01:26.648+03	12425
12428	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:28.059+03	2025-09-01 20:01:28.059+03	12426
12429	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:29.536+03	2025-09-01 20:01:29.536+03	12427
12430	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:30.734+03	2025-09-01 20:01:30.734+03	12428
12431	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:31.941+03	2025-09-01 20:01:31.941+03	12429
12432	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:33.064+03	2025-09-01 20:01:33.064+03	12430
12433	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:34.748+03	2025-09-01 20:01:34.748+03	12431
12434	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:36.481+03	2025-09-01 20:01:36.481+03	12432
12435	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:37.965+03	2025-09-01 20:01:37.965+03	12433
12436	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:39.279+03	2025-09-01 20:01:39.279+03	12434
12437	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:40.692+03	2025-09-01 20:01:40.692+03	12435
12438	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:41.952+03	2025-09-01 20:01:41.952+03	12436
12439	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:43.347+03	2025-09-01 20:01:43.347+03	12437
12440	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:45.162+03	2025-09-01 20:01:45.162+03	12438
12441	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:46.848+03	2025-09-01 20:01:46.848+03	12439
12442	-1.39478000	36.94079000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:01:46.951+03	2025-09-01 20:01:46.951+03	12440
12443	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:48.452+03	2025-09-01 20:01:48.452+03	12441
12444	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:49.686+03	2025-09-01 20:01:49.686+03	12442
12445	-0.53330000	37.45000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:51.233+03	2025-09-01 20:01:51.233+03	12443
12446	-0.44792000	39.64781000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:01:52.834+03	2025-09-01 20:01:52.834+03	12444
12447	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:54.054+03	2025-09-01 20:01:54.054+03	12445
12448	-0.42667000	39.66695000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:01:54.152+03	2025-09-01 20:01:54.152+03	12446
12449	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:56.075+03	2025-09-01 20:01:56.075+03	12447
12450	-0.44732000	39.64289000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:01:56.175+03	2025-09-01 20:01:56.175+03	12448
12451	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:57.72+03	2025-09-01 20:01:57.72+03	12449
12452	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:01:59.175+03	2025-09-01 20:01:59.175+03	12450
12453	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:00.835+03	2025-09-01 20:02:00.835+03	12451
12454	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:02.609+03	2025-09-01 20:02:02.609+03	12452
12455	-0.45292000	39.64500000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:03.918+03	2025-09-01 20:02:03.918+03	12453
12456	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:05.105+03	2025-09-01 20:02:05.105+03	12454
12457	-0.46587000	39.64987000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:05.264+03	2025-09-01 20:02:05.264+03	12455
12458	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:06.994+03	2025-09-01 20:02:06.994+03	12456
12459	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:08.571+03	2025-09-01 20:02:08.571+03	12457
12460	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:09.923+03	2025-09-01 20:02:09.923+03	12458
12461	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:11.013+03	2025-09-01 20:02:11.013+03	12459
12462	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:12.454+03	2025-09-01 20:02:12.454+03	12460
12463	-0.45006000	39.64578000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:14.309+03	2025-09-01 20:02:14.309+03	12461
12464	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:15.695+03	2025-09-01 20:02:15.695+03	12462
12465	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:17.546+03	2025-09-01 20:02:17.546+03	12463
12466	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:18.93+03	2025-09-01 20:02:18.93+03	12464
12467	-0.44603000	39.64379000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:19.023+03	2025-09-01 20:02:19.023+03	12465
12468	1.75101000	40.05594000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:19.11+03	2025-09-01 20:02:19.11+03	12466
12469	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:20.741+03	2025-09-01 20:02:20.741+03	12467
12470	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:21.97+03	2025-09-01 20:02:21.97+03	12468
12471	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:23.143+03	2025-09-01 20:02:23.143+03	12469
12472	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:24.179+03	2025-09-01 20:02:24.179+03	12470
12473	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:25.789+03	2025-09-01 20:02:25.789+03	12471
12474	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:27.12+03	2025-09-01 20:02:27.12+03	12472
12475	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:28.345+03	2025-09-01 20:02:28.345+03	12473
12476	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:29.673+03	2025-09-01 20:02:29.673+03	12474
12477	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:31.284+03	2025-09-01 20:02:31.284+03	12475
12478	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:32.564+03	2025-09-01 20:02:32.564+03	12476
12479	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:33.689+03	2025-09-01 20:02:33.689+03	12477
12480	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:35.065+03	2025-09-01 20:02:35.065+03	12478
12481	-0.42807000	39.65069000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:35.164+03	2025-09-01 20:02:35.164+03	12479
12482	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:36.675+03	2025-09-01 20:02:36.675+03	12480
12483	0.72978000	39.17195000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:36.817+03	2025-09-01 20:02:36.817+03	12481
12484	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:38.054+03	2025-09-01 20:02:38.054+03	12482
12485	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:39.244+03	2025-09-01 20:02:39.244+03	12483
12486	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:40.638+03	2025-09-01 20:02:40.638+03	12484
12487	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:42.451+03	2025-09-01 20:02:42.451+03	12485
12488	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:43.509+03	2025-09-01 20:02:43.509+03	12486
12489	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:44.739+03	2025-09-01 20:02:44.739+03	12487
12490	-0.44369000	39.66079000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:46.269+03	2025-09-01 20:02:46.269+03	12488
12491	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:47.387+03	2025-09-01 20:02:47.387+03	12489
12492	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:48.714+03	2025-09-01 20:02:48.714+03	12490
12493	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:50.186+03	2025-09-01 20:02:50.186+03	12491
12494	0.12265000	37.55971000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:02:51.71+03	2025-09-01 20:02:51.71+03	12492
12495	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:52.961+03	2025-09-01 20:02:52.961+03	12493
12496	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:54.257+03	2025-09-01 20:02:54.257+03	12494
12497	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:55.862+03	2025-09-01 20:02:55.862+03	12495
12498	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:57.46+03	2025-09-01 20:02:57.46+03	12496
12499	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:02:59.352+03	2025-09-01 20:02:59.352+03	12497
12500	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:01.18+03	2025-09-01 20:03:01.18+03	12498
12501	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:02.593+03	2025-09-01 20:03:02.593+03	12499
12502	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:04.002+03	2025-09-01 20:03:04.002+03	12500
12503	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:05.722+03	2025-09-01 20:03:05.722+03	12501
12504	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:06.874+03	2025-09-01 20:03:06.874+03	12502
12505	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:08.416+03	2025-09-01 20:03:08.416+03	12503
12506	1.74889000	40.05667000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:03:08.524+03	2025-09-01 20:03:08.524+03	12504
12507	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:10.379+03	2025-09-01 20:03:10.379+03	12505
12508	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:11.684+03	2025-09-01 20:03:11.684+03	12506
12509	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:13.015+03	2025-09-01 20:03:13.015+03	12507
12510	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:14.165+03	2025-09-01 20:03:14.165+03	12508
12511	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:15.617+03	2025-09-01 20:03:15.617+03	12509
12512	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:16.761+03	2025-09-01 20:03:16.761+03	12510
12513	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:18.097+03	2025-09-01 20:03:18.097+03	12511
12514	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:19.358+03	2025-09-01 20:03:19.358+03	12512
12515	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:21.034+03	2025-09-01 20:03:21.034+03	12513
12516	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:22.388+03	2025-09-01 20:03:22.388+03	12514
12517	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:23.502+03	2025-09-01 20:03:23.502+03	12515
12518	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:25.069+03	2025-09-01 20:03:25.069+03	12516
12519	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:26.207+03	2025-09-01 20:03:26.207+03	12517
12520	-1.27038000	36.74537000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:03:27.652+03	2025-09-01 20:03:27.652+03	12518
12521	-0.45000000	39.65000000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:28.656+03	2025-09-01 20:03:28.656+03	12519
12522	1.75666000	40.08475000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:03:29.904+03	2025-09-01 20:03:29.904+03	12520
12523	-1.06670000	34.46670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:31.611+03	2025-09-01 20:03:31.611+03	12521
12524	-0.68330000	34.76670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:33.264+03	2025-09-01 20:03:33.264+03	12522
12525	-0.68330000	34.76670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:34.701+03	2025-09-01 20:03:34.701+03	12523
12526	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:36.754+03	2025-09-01 20:03:36.754+03	12524
12527	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:38.266+03	2025-09-01 20:03:38.266+03	12525
12528	-0.54000000	34.50000000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:03:38.436+03	2025-09-01 20:03:38.436+03	12526
12529	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:39.779+03	2025-09-01 20:03:39.779+03	12527
12530	-1.06670000	34.46670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:41.441+03	2025-09-01 20:03:41.441+03	12528
12531	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:43.351+03	2025-09-01 20:03:43.351+03	12529
12532	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:44.683+03	2025-09-01 20:03:44.683+03	12530
12533	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:46.232+03	2025-09-01 20:03:46.232+03	12531
12534	-4.04350000	39.66820000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:47.809+03	2025-09-01 20:03:47.809+03	12532
12535	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:49.462+03	2025-09-01 20:03:49.462+03	12533
12536	-0.09366000	34.78063000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:03:51.095+03	2025-09-01 20:03:51.095+03	12534
12537	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:52.236+03	2025-09-01 20:03:52.236+03	12535
12538	0.56670000	34.56670000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:53.405+03	2025-09-01 20:03:53.405+03	12536
12539	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:54.702+03	2025-09-01 20:03:54.702+03	12537
12540	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:56.521+03	2025-09-01 20:03:56.521+03	12538
12541	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:03:58.267+03	2025-09-01 20:03:58.267+03	12539
12542	-0.10220000	34.76170000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:00.294+03	2025-09-01 20:04:00.294+03	12540
12543	-1.29210000	36.82190000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:02.529+03	2025-09-01 20:04:02.529+03	12541
12544	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:04.766+03	2025-09-01 20:04:04.766+03	12542
12545	0.33828000	37.57018000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:04:04.934+03	2025-09-01 20:04:04.934+03	12543
12546	0.35112700	37.58475000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:04:05.181+03	2025-09-01 20:04:05.181+03	12544
12547	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:07.288+03	2025-09-01 20:04:07.288+03	12545
12548	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:08.705+03	2025-09-01 20:04:08.705+03	12546
12549	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:10.462+03	2025-09-01 20:04:10.462+03	12547
12550	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:12.225+03	2025-09-01 20:04:12.225+03	12548
12551	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:14.058+03	2025-09-01 20:04:14.058+03	12549
12552	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:16.206+03	2025-09-01 20:04:16.206+03	12550
12553	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:18.292+03	2025-09-01 20:04:18.292+03	12551
12554	0.35106000	37.58317000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:04:18.434+03	2025-09-01 20:04:18.434+03	12552
12555	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:19.674+03	2025-09-01 20:04:19.674+03	12553
12556	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:21.503+03	2025-09-01 20:04:21.503+03	12554
12557	0.04568000	37.65362000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:04:23.031+03	2025-09-01 20:04:23.031+03	12555
12558	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:24.255+03	2025-09-01 20:04:24.255+03	12556
12559	-2.15929000	37.59477000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:04:24.386+03	2025-09-01 20:04:24.386+03	12557
12560	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:25.99+03	2025-09-01 20:04:25.99+03	12558
12561	3.93456000	41.85067000	2025-09-01	Healthcare Facilities Dataset	healthcare_facilities_json	2025-09-01 20:04:27.712+03	2025-09-01 20:04:27.712+03	12559
12562	0.35000000	37.58330000	2025-09-01	Enhanced ETL Pipeline (County Fallback)	county_based_fallback	2025-09-01 20:04:29.234+03	2025-09-01 20:04:29.234+03	12560
\.


--
-- TOC entry 4106 (class 0 OID 67422)
-- Dependencies: 279
-- Data for Name: facility_gbv_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facility_gbv_categories (id, created_at, created_by, facility_id, gbv_category_id) FROM stdin;
\.


--
-- TOC entry 4108 (class 0 OID 67428)
-- Dependencies: 281
-- Data for Name: facility_infrastructure; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facility_infrastructure (infrastructure_id, description, capacity, current_utilization, is_available, created_at, updated_at, condition_status_id, facility_id, infrastructure_type_id, created_by, is_active, updated_by) FROM stdin;
\.


--
-- TOC entry 4110 (class 0 OID 67436)
-- Dependencies: 283
-- Data for Name: facility_owners; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facility_owners (owner_id, owner_name, created_at, updated_at, created_by, facility_id, owner_type_id, updated_by) FROM stdin;
\.


--
-- TOC entry 4112 (class 0 OID 67442)
-- Dependencies: 285
-- Data for Name: facility_services; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facility_services (service_id, service_name, service_description, is_free, cost_range, currency, availability_hours, availability_days, appointment_required, is_active, created_at, updated_at, facility_id, service_category_id) FROM stdin;
26324	General Medical Services	Basic medical services provided at Baringo County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:33.923+03	2025-09-01 19:56:33.923+03	12201	11
26325	Emergency Response Services	Emergency response services at Baringo County Referral Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:56:33.929+03	2025-09-01 19:56:33.929+03	12201	27
26326	Counseling & Support Services	Counseling and support services at Baringo County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:33.934+03	2025-09-01 19:56:33.934+03	12201	20
26327	General Medical Services	Basic medical services provided at Eldama Ra Vine Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:35.286+03	2025-09-01 19:56:35.286+03	12202	11
26328	Emergency Response Services	Emergency response services at Eldama Ra Vine Sub-County Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:56:35.293+03	2025-09-01 19:56:35.293+03	12202	27
26329	Counseling & Support Services	Counseling and support services at Eldama Ra Vine Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:35.3+03	2025-09-01 19:56:35.3+03	12202	20
26330	General Medical Services	Basic medical services provided at Mercy Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:37.362+03	2025-09-01 19:56:37.362+03	12203	11
26331	Emergency Response Services	Emergency response services at Mercy Mission Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:56:37.372+03	2025-09-01 19:56:37.372+03	12203	27
26332	Counseling & Support Services	Counseling and support services at Mercy Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:37.38+03	2025-09-01 19:56:37.38+03	12203	20
26333	General Medical Services	Basic medical services provided at Kitabisi Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:37.807+03	2025-09-01 19:56:37.807+03	12204	11
26334	Counseling & Support Services	Counseling and support services at Kitabisi Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:37.818+03	2025-09-01 19:56:37.818+03	12204	20
26335	General Medical Services	Basic medical services provided at Kibuke Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:39.058+03	2025-09-01 19:56:39.058+03	12205	11
26336	Counseling & Support Services	Counseling and support services at Kibuke Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:39.065+03	2025-09-01 19:56:39.065+03	12205	20
26337	General Medical Services	Basic medical services provided at Muanda Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:39.124+03	2025-09-01 19:56:39.124+03	12206	11
26338	Counseling & Support Services	Counseling and support services at Muanda Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:39.133+03	2025-09-01 19:56:39.133+03	12206	20
26339	General Medical Services	Basic medical services provided at Nasianda Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.491+03	2025-09-01 19:56:40.491+03	12207	11
26340	Counseling & Support Services	Counseling and support services at Nasianda Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.5+03	2025-09-01 19:56:40.5+03	12207	20
26341	General Medical Services	Basic medical services provided at Ranje Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.588+03	2025-09-01 19:56:40.588+03	12208	11
26342	Counseling & Support Services	Counseling and support services at Ranje Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.594+03	2025-09-01 19:56:40.594+03	12208	20
26343	General Medical Services	Basic medical services provided at Kabula Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.638+03	2025-09-01 19:56:40.638+03	12209	11
26344	Counseling & Support Services	Counseling and support services at Kabula Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.645+03	2025-09-01 19:56:40.645+03	12209	20
26345	General Medical Services	Basic medical services provided at Bukokholo Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.707+03	2025-09-01 19:56:40.707+03	12210	11
26346	Counseling & Support Services	Counseling and support services at Bukokholo Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:40.716+03	2025-09-01 19:56:40.716+03	12210	20
26347	General Medical Services	Basic medical services provided at Bungoma G.K Prison Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:41.892+03	2025-09-01 19:56:41.892+03	12211	11
26348	Counseling & Support Services	Counseling and support services at Bungoma G.K Prison Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:41.899+03	2025-09-01 19:56:41.899+03	12211	20
26349	General Medical Services	Basic medical services provided at Mayanja Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:43.397+03	2025-09-01 19:56:43.397+03	12212	11
26350	Counseling & Support Services	Counseling and support services at Mayanja Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:43.404+03	2025-09-01 19:56:43.404+03	12212	20
26351	General Medical Services	Basic medical services provided at Webuye Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:43.458+03	2025-09-01 19:56:43.458+03	12213	11
26352	Emergency Response Services	Emergency response services at Webuye Sub-County Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:56:43.466+03	2025-09-01 19:56:43.466+03	12213	27
26353	Counseling & Support Services	Counseling and support services at Webuye Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:43.473+03	2025-09-01 19:56:43.473+03	12213	20
26354	General Medical Services	Basic medical services provided at Bungoma County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:44.736+03	2025-09-01 19:56:44.736+03	12214	11
26355	Emergency Response Services	Emergency response services at Bungoma County Referral Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:56:44.743+03	2025-09-01 19:56:44.743+03	12214	27
26356	Counseling & Support Services	Counseling and support services at Bungoma County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:44.75+03	2025-09-01 19:56:44.75+03	12214	20
26357	General Medical Services	Basic medical services provided at Bumula Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:46.342+03	2025-09-01 19:56:46.342+03	12215	11
26358	Emergency Response Services	Emergency response services at Bumula Sub-County Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:56:46.35+03	2025-09-01 19:56:46.35+03	12215	27
26359	Counseling & Support Services	Counseling and support services at Bumula Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:46.357+03	2025-09-01 19:56:46.357+03	12215	20
26360	General Medical Services	Basic medical services provided at Kimilili Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:47.745+03	2025-09-01 19:56:47.745+03	12216	11
26361	Emergency Response Services	Emergency response services at Kimilili Sub-County Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:56:47.752+03	2025-09-01 19:56:47.752+03	12216	27
26362	Counseling & Support Services	Counseling and support services at Kimilili Sub-County Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:47.759+03	2025-09-01 19:56:47.759+03	12216	20
26363	General Medical Services	Basic medical services provided at Kimaeti Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.414+03	2025-09-01 19:56:49.414+03	12217	11
26364	Counseling & Support Services	Counseling and support services at Kimaeti Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.424+03	2025-09-01 19:56:49.424+03	12217	20
26365	General Medical Services	Basic medical services provided at Mechimeru Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.484+03	2025-09-01 19:56:49.484+03	12218	11
26366	Counseling & Support Services	Counseling and support services at Mechimeru Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.495+03	2025-09-01 19:56:49.495+03	12218	20
26367	General Medical Services	Basic medical services provided at Bukembe Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.551+03	2025-09-01 19:56:49.551+03	12219	11
26368	Counseling & Support Services	Counseling and support services at Bukembe Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.557+03	2025-09-01 19:56:49.557+03	12219	20
26369	General Medical Services	Basic medical services provided at Bisunu Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.611+03	2025-09-01 19:56:49.611+03	12220	11
26370	Counseling & Support Services	Counseling and support services at Bisunu Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:49.619+03	2025-09-01 19:56:49.619+03	12220	20
26371	General Medical Services	Basic medical services provided at Tulienge Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:50.748+03	2025-09-01 19:56:50.748+03	12221	11
26372	Counseling & Support Services	Counseling and support services at Tulienge Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:50.755+03	2025-09-01 19:56:50.755+03	12221	20
26373	General Medical Services	Basic medical services provided at Bulondo Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:52.033+03	2025-09-01 19:56:52.033+03	12222	11
26374	Counseling & Support Services	Counseling and support services at Bulondo Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:52.04+03	2025-09-01 19:56:52.04+03	12222	20
26375	General Medical Services	Basic medical services provided at Nabukhisa Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:52.111+03	2025-09-01 19:56:52.111+03	12223	11
26376	Counseling & Support Services	Counseling and support services at Nabukhisa Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:52.119+03	2025-09-01 19:56:52.119+03	12223	20
26377	General Medical Services	Basic medical services provided at Myanga Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:53.455+03	2025-09-01 19:56:53.455+03	12224	11
26378	Counseling & Support Services	Counseling and support services at Myanga Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:53.49+03	2025-09-01 19:56:53.49+03	12224	20
26379	General Medical Services	Basic medical services provided at Kamusinde Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:55.072+03	2025-09-01 19:56:55.072+03	12225	11
26380	Counseling & Support Services	Counseling and support services at Kamusinde Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:55.086+03	2025-09-01 19:56:55.086+03	12225	20
26381	General Medical Services	Basic medical services provided at Kisawaiyi Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:56.295+03	2025-09-01 19:56:56.295+03	12226	11
26382	Counseling & Support Services	Counseling and support services at Kisawaiyi Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:56.309+03	2025-09-01 19:56:56.309+03	12226	20
26383	General Medical Services	Basic medical services provided at Kipsabula Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:57.519+03	2025-09-01 19:56:57.519+03	12227	11
26384	Counseling & Support Services	Counseling and support services at Kipsabula Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:57.535+03	2025-09-01 19:56:57.535+03	12227	20
26385	General Medical Services	Basic medical services provided at Samoya Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:58.729+03	2025-09-01 19:56:58.729+03	12228	11
26386	Counseling & Support Services	Counseling and support services at Samoya Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:58.737+03	2025-09-01 19:56:58.737+03	12228	20
26387	General Medical Services	Basic medical services provided at Butieli Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:59.851+03	2025-09-01 19:56:59.851+03	12229	11
26388	Counseling & Support Services	Counseling and support services at Butieli Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:56:59.863+03	2025-09-01 19:56:59.863+03	12229	20
26389	General Medical Services	Basic medical services provided at Siritanyi Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:01.359+03	2025-09-01 19:57:01.359+03	12230	11
26390	Counseling & Support Services	Counseling and support services at Siritanyi Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:01.368+03	2025-09-01 19:57:01.368+03	12230	20
26391	General Medical Services	Basic medical services provided at Kongit Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:02.612+03	2025-09-01 19:57:02.612+03	12231	11
26392	Counseling & Support Services	Counseling and support services at Kongit Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:02.62+03	2025-09-01 19:57:02.62+03	12231	20
26393	General Medical Services	Basic medical services provided at Makololwe Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:04.345+03	2025-09-01 19:57:04.345+03	12232	11
26394	Counseling & Support Services	Counseling and support services at Makololwe Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:04.354+03	2025-09-01 19:57:04.354+03	12232	20
26395	General Medical Services	Basic medical services provided at Makunga Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:05.984+03	2025-09-01 19:57:05.984+03	12233	11
26396	Counseling & Support Services	Counseling and support services at Makunga Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:05.991+03	2025-09-01 19:57:05.991+03	12233	20
26397	General Medical Services	Basic medical services provided at Namirembe Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:07.904+03	2025-09-01 19:57:07.904+03	12234	11
26398	Counseling & Support Services	Counseling and support services at Namirembe Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:07.913+03	2025-09-01 19:57:07.913+03	12234	20
26399	General Medical Services	Basic medical services provided at Fathers Love Foundation Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:09.087+03	2025-09-01 19:57:09.087+03	12235	11
26400	Counseling & Support Services	Counseling and support services at Fathers Love Foundation Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:09.093+03	2025-09-01 19:57:09.093+03	12235	20
26401	General Medical Services	Basic medical services provided at Mission Of Mercy Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:10.557+03	2025-09-01 19:57:10.557+03	12236	11
26402	Emergency Response Services	Emergency response services at Mission Of Mercy Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:10.564+03	2025-09-01 19:57:10.564+03	12236	27
26403	Counseling & Support Services	Counseling and support services at Mission Of Mercy Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:10.572+03	2025-09-01 19:57:10.572+03	12236	20
26404	General Medical Services	Basic medical services provided at St Anthonys Kibabii Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:10.634+03	2025-09-01 19:57:10.634+03	12237	11
26405	Counseling & Support Services	Counseling and support services at St Anthonys Kibabii Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:10.642+03	2025-09-01 19:57:10.642+03	12237	20
26406	General Medical Services	Basic medical services provided at St. Damiano Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:12.234+03	2025-09-01 19:57:12.234+03	12238	11
26407	Emergency Response Services	Emergency response services at St. Damiano Mission Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:12.245+03	2025-09-01 19:57:12.245+03	12238	27
26408	Counseling & Support Services	Counseling and support services at St. Damiano Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:12.266+03	2025-09-01 19:57:12.266+03	12238	20
26409	General Medical Services	Basic medical services provided at Ack Dr. Pike Roper Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:13.841+03	2025-09-01 19:57:13.841+03	12239	11
26410	Counseling & Support Services	Counseling and support services at Ack Dr. Pike Roper Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:13.861+03	2025-09-01 19:57:13.861+03	12239	20
26411	General Medical Services	Basic medical services provided at Carmel Dispensary Kimwanga	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:15.3+03	2025-09-01 19:57:15.3+03	12240	11
26412	Counseling & Support Services	Counseling and support services at Carmel Dispensary Kimwanga	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:15.307+03	2025-09-01 19:57:15.307+03	12240	20
26413	General Medical Services	Basic medical services provided at New Elgon View Medical Cottage	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:16.754+03	2025-09-01 19:57:16.754+03	12241	11
26414	Counseling & Support Services	Counseling and support services at New Elgon View Medical Cottage	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:16.761+03	2025-09-01 19:57:16.761+03	12241	20
26415	General Medical Services	Basic medical services provided at Machwele Friends Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:18.913+03	2025-09-01 19:57:18.913+03	12242	11
26416	Counseling & Support Services	Counseling and support services at Machwele Friends Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:18.936+03	2025-09-01 19:57:18.936+03	12242	20
26417	General Medical Services	Basic medical services provided at Nzoia Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:20.589+03	2025-09-01 19:57:20.589+03	12243	11
26418	Counseling & Support Services	Counseling and support services at Nzoia Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:20.6+03	2025-09-01 19:57:20.6+03	12243	20
26419	General Medical Services	Basic medical services provided at The Aga Khan Hospital Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:20.707+03	2025-09-01 19:57:20.707+03	12244	11
26420	Emergency Response Services	Emergency response services at The Aga Khan Hospital Bungoma	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:20.719+03	2025-09-01 19:57:20.719+03	12244	27
26421	Counseling & Support Services	Counseling and support services at The Aga Khan Hospital Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:20.73+03	2025-09-01 19:57:20.73+03	12244	20
26422	General Medical Services	Basic medical services provided at Bungoma West Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:22.068+03	2025-09-01 19:57:22.068+03	12245	11
26423	Emergency Response Services	Emergency response services at Bungoma West Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:22.075+03	2025-09-01 19:57:22.075+03	12245	27
26424	Counseling & Support Services	Counseling and support services at Bungoma West Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:22.083+03	2025-09-01 19:57:22.083+03	12245	20
26425	General Medical Services	Basic medical services provided at Khalaba Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:23.773+03	2025-09-01 19:57:23.773+03	12246	11
26426	Counseling & Support Services	Counseling and support services at Khalaba Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:23.78+03	2025-09-01 19:57:23.78+03	12246	20
26427	General Medical Services	Basic medical services provided at Bungoma Wema Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:23.852+03	2025-09-01 19:57:23.852+03	12247	11
26428	Counseling & Support Services	Counseling and support services at Bungoma Wema Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:23.859+03	2025-09-01 19:57:23.859+03	12247	20
26429	General Medical Services	Basic medical services provided at St. James Opticals	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:25.178+03	2025-09-01 19:57:25.178+03	12248	11
26430	Counseling & Support Services	Counseling and support services at St. James Opticals	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:25.185+03	2025-09-01 19:57:25.185+03	12248	20
26431	General Medical Services	Basic medical services provided at Kanduyi Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:26.499+03	2025-09-01 19:57:26.499+03	12249	11
26432	Counseling & Support Services	Counseling and support services at Kanduyi Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:26.507+03	2025-09-01 19:57:26.507+03	12249	20
26433	General Medical Services	Basic medical services provided at Trinity Opticals Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:28.167+03	2025-09-01 19:57:28.167+03	12250	11
26434	Counseling & Support Services	Counseling and support services at Trinity Opticals Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:28.174+03	2025-09-01 19:57:28.174+03	12250	20
26435	General Medical Services	Basic medical services provided at Bliss Healthcare Limited Kimilili	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:29.754+03	2025-09-01 19:57:29.754+03	12251	11
26436	Counseling & Support Services	Counseling and support services at Bliss Healthcare Limited Kimilili	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:29.762+03	2025-09-01 19:57:29.762+03	12251	20
26437	General Medical Services	Basic medical services provided at Bliss Healthcare Ltd Webuye	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:31.218+03	2025-09-01 19:57:31.218+03	12252	11
26438	Counseling & Support Services	Counseling and support services at Bliss Healthcare Ltd Webuye	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:31.227+03	2025-09-01 19:57:31.227+03	12252	20
26439	General Medical Services	Basic medical services provided at Nabuala Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:32.598+03	2025-09-01 19:57:32.598+03	12253	11
26440	Emergency Response Services	Emergency response services at Nabuala Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:32.608+03	2025-09-01 19:57:32.608+03	12253	27
26441	Counseling & Support Services	Counseling and support services at Nabuala Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:32.616+03	2025-09-01 19:57:32.616+03	12253	20
26442	General Medical Services	Basic medical services provided at Fountain Healthcare Ltd Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:33.652+03	2025-09-01 19:57:33.652+03	12254	11
26443	Counseling & Support Services	Counseling and support services at Fountain Healthcare Ltd Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:33.661+03	2025-09-01 19:57:33.661+03	12254	20
26444	General Medical Services	Basic medical services provided at Mpeli Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:35.219+03	2025-09-01 19:57:35.219+03	12255	11
26445	Counseling & Support Services	Counseling and support services at Mpeli Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:35.23+03	2025-09-01 19:57:35.23+03	12255	20
26446	General Medical Services	Basic medical services provided at Lifecare Hospitals Bungoma Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:36.184+03	2025-09-01 19:57:36.184+03	12256	11
26447	Emergency Response Services	Emergency response services at Lifecare Hospitals Bungoma Ltd	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:36.194+03	2025-09-01 19:57:36.194+03	12256	27
26448	Counseling & Support Services	Counseling and support services at Lifecare Hospitals Bungoma Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:36.2+03	2025-09-01 19:57:36.2+03	12256	20
26449	General Medical Services	Basic medical services provided at Zion Medical Centre - Bungoma Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:37.871+03	2025-09-01 19:57:37.871+03	12257	11
26450	Counseling & Support Services	Counseling and support services at Zion Medical Centre - Bungoma Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:37.882+03	2025-09-01 19:57:37.882+03	12257	20
26451	General Medical Services	Basic medical services provided at Kory Family Hospital Kimilili	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:39.23+03	2025-09-01 19:57:39.23+03	12258	11
26452	Emergency Response Services	Emergency response services at Kory Family Hospital Kimilili	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:39.238+03	2025-09-01 19:57:39.238+03	12258	27
26453	Counseling & Support Services	Counseling and support services at Kory Family Hospital Kimilili	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:39.247+03	2025-09-01 19:57:39.247+03	12258	20
26454	General Medical Services	Basic medical services provided at Bungoma West Hospital Town Annex Branch	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:40.929+03	2025-09-01 19:57:40.929+03	12259	11
26455	Emergency Response Services	Emergency response services at Bungoma West Hospital Town Annex Branch	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:40.937+03	2025-09-01 19:57:40.937+03	12259	27
26456	Counseling & Support Services	Counseling and support services at Bungoma West Hospital Town Annex Branch	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:40.946+03	2025-09-01 19:57:40.946+03	12259	20
26457	General Medical Services	Basic medical services provided at Brillian Doctors Plaza Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:43.09+03	2025-09-01 19:57:43.09+03	12260	11
26458	Emergency Response Services	Emergency response services at Brillian Doctors Plaza Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:43.098+03	2025-09-01 19:57:43.098+03	12260	27
26459	Counseling & Support Services	Counseling and support services at Brillian Doctors Plaza Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:43.108+03	2025-09-01 19:57:43.108+03	12260	20
26460	General Medical Services	Basic medical services provided at Mercal Healthcare Bukembe	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:44.643+03	2025-09-01 19:57:44.643+03	12261	11
26461	Counseling & Support Services	Counseling and support services at Mercal Healthcare Bukembe	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:44.65+03	2025-09-01 19:57:44.65+03	12261	20
26462	General Medical Services	Basic medical services provided at The Dawameds Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:46.126+03	2025-09-01 19:57:46.126+03	12262	11
26463	Emergency Response Services	Emergency response services at The Dawameds Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:46.134+03	2025-09-01 19:57:46.134+03	12262	27
26464	Counseling & Support Services	Counseling and support services at The Dawameds Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:46.144+03	2025-09-01 19:57:46.144+03	12262	20
26465	General Medical Services	Basic medical services provided at Chrizah Medical Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:47.799+03	2025-09-01 19:57:47.799+03	12263	11
26466	Counseling & Support Services	Counseling and support services at Chrizah Medical Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:47.808+03	2025-09-01 19:57:47.808+03	12263	20
26467	General Medical Services	Basic medical services provided at Global Homecare Ltd Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:50.621+03	2025-09-01 19:57:50.621+03	12264	11
26468	Counseling & Support Services	Counseling and support services at Global Homecare Ltd Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:50.645+03	2025-09-01 19:57:50.645+03	12264	20
26469	General Medical Services	Basic medical services provided at Springwell Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:52.447+03	2025-09-01 19:57:52.447+03	12265	11
26470	Counseling & Support Services	Counseling and support services at Springwell Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:52.454+03	2025-09-01 19:57:52.454+03	12265	20
26471	General Medical Services	Basic medical services provided at Healridge Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:54.262+03	2025-09-01 19:57:54.262+03	12266	11
26472	Counseling & Support Services	Counseling and support services at Healridge Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:54.269+03	2025-09-01 19:57:54.269+03	12266	20
26473	General Medical Services	Basic medical services provided at Mangs Health Care Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:55.549+03	2025-09-01 19:57:55.549+03	12267	11
26474	Counseling & Support Services	Counseling and support services at Mangs Health Care Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:55.556+03	2025-09-01 19:57:55.556+03	12267	20
26475	General Medical Services	Basic medical services provided at Wanda Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:57.251+03	2025-09-01 19:57:57.251+03	12268	11
26476	Counseling & Support Services	Counseling and support services at Wanda Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:57.258+03	2025-09-01 19:57:57.258+03	12268	20
26477	General Medical Services	Basic medical services provided at The Hopkins Crescent Hospitals Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:58.468+03	2025-09-01 19:57:58.468+03	12269	11
26478	Emergency Response Services	Emergency response services at The Hopkins Crescent Hospitals Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:57:58.475+03	2025-09-01 19:57:58.475+03	12269	27
26479	Counseling & Support Services	Counseling and support services at The Hopkins Crescent Hospitals Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:57:58.485+03	2025-09-01 19:57:58.485+03	12269	20
26480	General Medical Services	Basic medical services provided at Bungoma Childrens Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:00.584+03	2025-09-01 19:58:00.584+03	12270	11
26481	Counseling & Support Services	Counseling and support services at Bungoma Childrens Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:00.59+03	2025-09-01 19:58:00.59+03	12270	20
26482	General Medical Services	Basic medical services provided at Saint Jude Thaddeo Mabanga Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:02.379+03	2025-09-01 19:58:02.379+03	12271	11
26483	Counseling & Support Services	Counseling and support services at Saint Jude Thaddeo Mabanga Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:02.387+03	2025-09-01 19:58:02.387+03	12271	20
26484	General Medical Services	Basic medical services provided at Buckner Family Hope Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:04.026+03	2025-09-01 19:58:04.026+03	12272	11
26485	Counseling & Support Services	Counseling and support services at Buckner Family Hope Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:04.036+03	2025-09-01 19:58:04.036+03	12272	20
26486	General Medical Services	Basic medical services provided at Oasis Doctors Plaza Webuye Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:05.904+03	2025-09-01 19:58:05.904+03	12273	11
26487	Counseling & Support Services	Counseling and support services at Oasis Doctors Plaza Webuye Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:05.915+03	2025-09-01 19:58:05.915+03	12273	20
26488	General Medical Services	Basic medical services provided at The Dawameds Hospital Limited-Sirisia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:07.637+03	2025-09-01 19:58:07.637+03	12274	11
26489	Emergency Response Services	Emergency response services at The Dawameds Hospital Limited-Sirisia	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:58:07.643+03	2025-09-01 19:58:07.643+03	12274	27
26490	Counseling & Support Services	Counseling and support services at The Dawameds Hospital Limited-Sirisia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:07.654+03	2025-09-01 19:58:07.654+03	12274	20
26491	General Medical Services	Basic medical services provided at Bungoma Adorah Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:09.195+03	2025-09-01 19:58:09.195+03	12275	11
26492	Counseling & Support Services	Counseling and support services at Bungoma Adorah Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:09.203+03	2025-09-01 19:58:09.203+03	12275	20
26493	General Medical Services	Basic medical services provided at Afya Space Consultancy Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:10.84+03	2025-09-01 19:58:10.84+03	12276	11
26494	Counseling & Support Services	Counseling and support services at Afya Space Consultancy Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:10.849+03	2025-09-01 19:58:10.849+03	12276	20
26495	General Medical Services	Basic medical services provided at Rozajem Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:12.802+03	2025-09-01 19:58:12.802+03	12277	11
26496	Counseling & Support Services	Counseling and support services at Rozajem Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:12.818+03	2025-09-01 19:58:12.818+03	12277	20
26497	General Medical Services	Basic medical services provided at Al-Ihsaan Health Centre Kimaeti	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:14.104+03	2025-09-01 19:58:14.104+03	12278	11
26498	Counseling & Support Services	Counseling and support services at Al-Ihsaan Health Centre Kimaeti	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:14.111+03	2025-09-01 19:58:14.111+03	12278	20
26499	General Medical Services	Basic medical services provided at Connection Health Services Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:15.768+03	2025-09-01 19:58:15.768+03	12279	11
26500	Counseling & Support Services	Counseling and support services at Connection Health Services Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:15.775+03	2025-09-01 19:58:15.775+03	12279	20
26501	General Medical Services	Basic medical services provided at St.Pauls Kibabii Ttc Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:17.393+03	2025-09-01 19:58:17.393+03	12280	11
26502	Counseling & Support Services	Counseling and support services at St.Pauls Kibabii Ttc Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:17.402+03	2025-09-01 19:58:17.402+03	12280	20
26503	General Medical Services	Basic medical services provided at Kimwanga Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:19.105+03	2025-09-01 19:58:19.105+03	12281	11
26504	Counseling & Support Services	Counseling and support services at Kimwanga Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:19.114+03	2025-09-01 19:58:19.114+03	12281	20
26505	General Medical Services	Basic medical services provided at Samaritan Eye  Retina Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:20.405+03	2025-09-01 19:58:20.405+03	12282	11
26506	Counseling & Support Services	Counseling and support services at Samaritan Eye  Retina Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:20.412+03	2025-09-01 19:58:20.412+03	12282	20
26507	General Medical Services	Basic medical services provided at Transelgon Healthcare Ltd - Cheptais	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:22.225+03	2025-09-01 19:58:22.225+03	12283	11
26508	Counseling & Support Services	Counseling and support services at Transelgon Healthcare Ltd - Cheptais	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:22.233+03	2025-09-01 19:58:22.233+03	12283	20
26509	General Medical Services	Basic medical services provided at Morimed Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:23.923+03	2025-09-01 19:58:23.923+03	12284	11
26510	Counseling & Support Services	Counseling and support services at Morimed Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:23.931+03	2025-09-01 19:58:23.931+03	12284	20
26511	General Medical Services	Basic medical services provided at Melita Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:25.738+03	2025-09-01 19:58:25.738+03	12285	11
26512	Counseling & Support Services	Counseling and support services at Melita Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:25.757+03	2025-09-01 19:58:25.757+03	12285	20
26513	General Medical Services	Basic medical services provided at Bungoma Dental  Eye Care Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:27.327+03	2025-09-01 19:58:27.327+03	12286	11
26514	Counseling & Support Services	Counseling and support services at Bungoma Dental  Eye Care Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:27.336+03	2025-09-01 19:58:27.336+03	12286	20
26515	General Medical Services	Basic medical services provided at Elephant Dental Limited-Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:29.141+03	2025-09-01 19:58:29.141+03	12287	11
26516	Counseling & Support Services	Counseling and support services at Elephant Dental Limited-Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:29.149+03	2025-09-01 19:58:29.149+03	12287	20
26517	General Medical Services	Basic medical services provided at Equity Afia Limited- Bungoma Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:30.647+03	2025-09-01 19:58:30.647+03	12288	11
26518	Counseling & Support Services	Counseling and support services at Equity Afia Limited- Bungoma Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:30.654+03	2025-09-01 19:58:30.654+03	12288	20
26519	General Medical Services	Basic medical services provided at Eliane Royal Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:32.389+03	2025-09-01 19:58:32.389+03	12289	11
26520	Emergency Response Services	Emergency response services at Eliane Royal Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:58:32.398+03	2025-09-01 19:58:32.398+03	12289	27
26521	Counseling & Support Services	Counseling and support services at Eliane Royal Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:32.413+03	2025-09-01 19:58:32.413+03	12289	20
26522	General Medical Services	Basic medical services provided at Racia Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:33.703+03	2025-09-01 19:58:33.703+03	12290	11
26523	Emergency Response Services	Emergency response services at Racia Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:58:33.711+03	2025-09-01 19:58:33.711+03	12290	27
26524	Counseling & Support Services	Counseling and support services at Racia Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:33.719+03	2025-09-01 19:58:33.719+03	12290	20
26525	General Medical Services	Basic medical services provided at Chad Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:34.811+03	2025-09-01 19:58:34.811+03	12291	11
26526	Counseling & Support Services	Counseling and support services at Chad Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:34.819+03	2025-09-01 19:58:34.819+03	12291	20
26527	General Medical Services	Basic medical services provided at Myanga Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:36.233+03	2025-09-01 19:58:36.233+03	12292	11
26528	Counseling & Support Services	Counseling and support services at Myanga Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:36.24+03	2025-09-01 19:58:36.24+03	12292	20
26529	General Medical Services	Basic medical services provided at Olympia Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:37.732+03	2025-09-01 19:58:37.732+03	12293	11
26530	Counseling & Support Services	Counseling and support services at Olympia Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:37.739+03	2025-09-01 19:58:37.739+03	12293	20
26531	General Medical Services	Basic medical services provided at Nzoia Sugar Company	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:38.866+03	2025-09-01 19:58:38.866+03	12294	11
26532	Counseling & Support Services	Counseling and support services at Nzoia Sugar Company	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:38.874+03	2025-09-01 19:58:38.874+03	12294	20
26533	General Medical Services	Basic medical services provided at Edesa Medicare Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:40.351+03	2025-09-01 19:58:40.351+03	12295	11
26534	Counseling & Support Services	Counseling and support services at Edesa Medicare Bungoma	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:40.359+03	2025-09-01 19:58:40.359+03	12295	20
26535	General Medical Services	Basic medical services provided at Your Family Cfw Community Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:41.807+03	2025-09-01 19:58:41.807+03	12296	11
26536	Counseling & Support Services	Counseling and support services at Your Family Cfw Community Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:41.815+03	2025-09-01 19:58:41.815+03	12296	20
26537	General Medical Services	Basic medical services provided at Busia County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:43.643+03	2025-09-01 19:58:43.643+03	12297	11
26538	Emergency Response Services	Emergency response services at Busia County Referral Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:58:43.652+03	2025-09-01 19:58:43.652+03	12297	27
26539	Counseling & Support Services	Counseling and support services at Busia County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:43.66+03	2025-09-01 19:58:43.66+03	12297	20
26540	General Medical Services	Basic medical services provided at Kari Trc Alupe Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:45.095+03	2025-09-01 19:58:45.095+03	12298	11
26541	Emergency Response Services	Emergency response services at Kari Trc Alupe Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:58:45.103+03	2025-09-01 19:58:45.103+03	12298	27
26542	Counseling & Support Services	Counseling and support services at Kari Trc Alupe Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:45.111+03	2025-09-01 19:58:45.111+03	12298	20
26543	General Medical Services	Basic medical services provided at Holy Family Hospital Nangina	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:46.405+03	2025-09-01 19:58:46.405+03	12299	11
26544	Emergency Response Services	Emergency response services at Holy Family Hospital Nangina	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:58:46.415+03	2025-09-01 19:58:46.415+03	12299	27
26545	Counseling & Support Services	Counseling and support services at Holy Family Hospital Nangina	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:46.423+03	2025-09-01 19:58:46.423+03	12299	20
26546	General Medical Services	Basic medical services provided at Cornerstone Baptist	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:46.495+03	2025-09-01 19:58:46.495+03	12300	11
26547	Counseling & Support Services	Counseling and support services at Cornerstone Baptist	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:46.503+03	2025-09-01 19:58:46.503+03	12300	20
26548	General Medical Services	Basic medical services provided at Tanaka Nursing Home Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:47.872+03	2025-09-01 19:58:47.872+03	12301	11
26549	Counseling & Support Services	Counseling and support services at Tanaka Nursing Home Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:47.883+03	2025-09-01 19:58:47.883+03	12301	20
26550	General Medical Services	Basic medical services provided at New Busia Maternity  Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:49.27+03	2025-09-01 19:58:49.27+03	12302	11
26551	Counseling & Support Services	Counseling and support services at New Busia Maternity  Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:49.279+03	2025-09-01 19:58:49.279+03	12302	20
26552	General Medical Services	Basic medical services provided at Fahelma Cfw Community Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:49.356+03	2025-09-01 19:58:49.356+03	12303	11
26553	Counseling & Support Services	Counseling and support services at Fahelma Cfw Community Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:49.367+03	2025-09-01 19:58:49.367+03	12303	20
26554	General Medical Services	Basic medical services provided at Bumala Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:50.785+03	2025-09-01 19:58:50.785+03	12304	11
26555	Counseling & Support Services	Counseling and support services at Bumala Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:50.793+03	2025-09-01 19:58:50.793+03	12304	20
26556	General Medical Services	Basic medical services provided at Namenya Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:50.871+03	2025-09-01 19:58:50.871+03	12305	11
26557	Counseling & Support Services	Counseling and support services at Namenya Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:50.88+03	2025-09-01 19:58:50.88+03	12305	20
26558	General Medical Services	Basic medical services provided at Pesi Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:50.935+03	2025-09-01 19:58:50.935+03	12306	11
26559	Counseling & Support Services	Counseling and support services at Pesi Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:50.943+03	2025-09-01 19:58:50.943+03	12306	20
26560	General Medical Services	Basic medical services provided at The Aga Khan Hospital - Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:51.005+03	2025-09-01 19:58:51.005+03	12307	11
26561	Emergency Response Services	Emergency response services at The Aga Khan Hospital - Busia	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:58:51.013+03	2025-09-01 19:58:51.013+03	12307	27
26562	Counseling & Support Services	Counseling and support services at The Aga Khan Hospital - Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:51.021+03	2025-09-01 19:58:51.021+03	12307	20
26563	General Medical Services	Basic medical services provided at Feith Medical Clinic Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:52.336+03	2025-09-01 19:58:52.336+03	12308	11
26564	Counseling & Support Services	Counseling and support services at Feith Medical Clinic Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:52.346+03	2025-09-01 19:58:52.346+03	12308	20
26565	General Medical Services	Basic medical services provided at Busia Equator Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:53.827+03	2025-09-01 19:58:53.827+03	12309	11
26566	Counseling & Support Services	Counseling and support services at Busia Equator Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:53.836+03	2025-09-01 19:58:53.836+03	12309	20
26567	General Medical Services	Basic medical services provided at Busia Base Boarder Faith Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:55.648+03	2025-09-01 19:58:55.648+03	12310	11
26568	Counseling & Support Services	Counseling and support services at Busia Base Boarder Faith Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:55.66+03	2025-09-01 19:58:55.66+03	12310	20
26569	General Medical Services	Basic medical services provided at Stirling Healthcare Consultants	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:57.802+03	2025-09-01 19:58:57.802+03	12311	11
26570	Counseling & Support Services	Counseling and support services at Stirling Healthcare Consultants	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:57.809+03	2025-09-01 19:58:57.809+03	12311	20
26571	General Medical Services	Basic medical services provided at Busia Healthsidelab Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:59.672+03	2025-09-01 19:58:59.672+03	12312	11
26572	Counseling & Support Services	Counseling and support services at Busia Healthsidelab Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:58:59.679+03	2025-09-01 19:58:59.679+03	12312	20
26573	General Medical Services	Basic medical services provided at Bunyala Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:01.618+03	2025-09-01 19:59:01.618+03	12313	11
26574	Counseling & Support Services	Counseling and support services at Bunyala Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:01.629+03	2025-09-01 19:59:01.629+03	12313	20
26575	General Medical Services	Basic medical services provided at Optex Opticians Ltd - Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:03.432+03	2025-09-01 19:59:03.432+03	12314	11
26576	Counseling & Support Services	Counseling and support services at Optex Opticians Ltd - Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:03.444+03	2025-09-01 19:59:03.444+03	12314	20
26577	General Medical Services	Basic medical services provided at Visiongate Eye Care Consultant	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:04.846+03	2025-09-01 19:59:04.846+03	12315	11
26578	Counseling & Support Services	Counseling and support services at Visiongate Eye Care Consultant	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:04.857+03	2025-09-01 19:59:04.857+03	12315	20
26579	General Medical Services	Basic medical services provided at Zurri Cottage Healthcare	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:06.415+03	2025-09-01 19:59:06.415+03	12316	11
26580	Counseling & Support Services	Counseling and support services at Zurri Cottage Healthcare	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:06.423+03	2025-09-01 19:59:06.423+03	12316	20
26581	General Medical Services	Basic medical services provided at Minallahi Medicare	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:07.835+03	2025-09-01 19:59:07.835+03	12317	11
26582	Counseling & Support Services	Counseling and support services at Minallahi Medicare	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:07.846+03	2025-09-01 19:59:07.846+03	12317	20
26583	General Medical Services	Basic medical services provided at Bliss Healthcare Ltd Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:09.643+03	2025-09-01 19:59:09.643+03	12318	11
26584	Counseling & Support Services	Counseling and support services at Bliss Healthcare Ltd Busia	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:09.65+03	2025-09-01 19:59:09.65+03	12318	20
26585	General Medical Services	Basic medical services provided at Amane Cottage Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:11.038+03	2025-09-01 19:59:11.038+03	12319	11
26586	Emergency Response Services	Emergency response services at Amane Cottage Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:11.049+03	2025-09-01 19:59:11.049+03	12319	27
26587	Counseling & Support Services	Counseling and support services at Amane Cottage Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:11.059+03	2025-09-01 19:59:11.059+03	12319	20
26588	General Medical Services	Basic medical services provided at Lumola Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:12.354+03	2025-09-01 19:59:12.354+03	12320	11
26589	Counseling & Support Services	Counseling and support services at Lumola Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:12.363+03	2025-09-01 19:59:12.363+03	12320	20
26590	General Medical Services	Basic medical services provided at Nassi Hospitals	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:13.654+03	2025-09-01 19:59:13.654+03	12321	11
26591	Emergency Response Services	Emergency response services at Nassi Hospitals	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:13.662+03	2025-09-01 19:59:13.662+03	12321	27
26592	Counseling & Support Services	Counseling and support services at Nassi Hospitals	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:13.669+03	2025-09-01 19:59:13.669+03	12321	20
26593	General Medical Services	Basic medical services provided at Medspar Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:15.241+03	2025-09-01 19:59:15.241+03	12322	11
26594	Counseling & Support Services	Counseling and support services at Medspar Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:15.256+03	2025-09-01 19:59:15.256+03	12322	20
26595	General Medical Services	Basic medical services provided at Turning Point Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:16.484+03	2025-09-01 19:59:16.484+03	12323	11
26596	Counseling & Support Services	Counseling and support services at Turning Point Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:16.493+03	2025-09-01 19:59:16.493+03	12323	20
26597	General Medical Services	Basic medical services provided at Busia Medical Specialists And Diagnostic Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:17.984+03	2025-09-01 19:59:17.984+03	12324	11
26598	Counseling & Support Services	Counseling and support services at Busia Medical Specialists And Diagnostic Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:17.993+03	2025-09-01 19:59:17.993+03	12324	20
26599	General Medical Services	Basic medical services provided at Brilliance Care Medical Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:19.66+03	2025-09-01 19:59:19.66+03	12325	11
26600	Emergency Response Services	Emergency response services at Brilliance Care Medical Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:19.669+03	2025-09-01 19:59:19.669+03	12325	27
26601	Counseling & Support Services	Counseling and support services at Brilliance Care Medical Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:19.676+03	2025-09-01 19:59:19.676+03	12325	20
26602	General Medical Services	Basic medical services provided at Ganga Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:21.207+03	2025-09-01 19:59:21.207+03	12326	11
26603	Counseling & Support Services	Counseling and support services at Ganga Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:21.214+03	2025-09-01 19:59:21.214+03	12326	20
26604	General Medical Services	Basic medical services provided at Leben Medical Service-Busibwabo	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:22.461+03	2025-09-01 19:59:22.462+03	12327	11
26605	Counseling & Support Services	Counseling and support services at Leben Medical Service-Busibwabo	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:22.469+03	2025-09-01 19:59:22.469+03	12327	20
26606	General Medical Services	Basic medical services provided at Tomaps Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:23.964+03	2025-09-01 19:59:23.964+03	12328	11
26607	Counseling & Support Services	Counseling and support services at Tomaps Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:23.972+03	2025-09-01 19:59:23.972+03	12328	20
26608	General Medical Services	Basic medical services provided at Brimaxa Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:25.247+03	2025-09-01 19:59:25.247+03	12329	11
26609	Emergency Response Services	Emergency response services at Brimaxa Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:25.256+03	2025-09-01 19:59:25.256+03	12329	27
26610	Counseling & Support Services	Counseling and support services at Brimaxa Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:25.265+03	2025-09-01 19:59:25.265+03	12329	20
26611	General Medical Services	Basic medical services provided at Good Hope Health Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:26.546+03	2025-09-01 19:59:26.546+03	12330	11
26612	Counseling & Support Services	Counseling and support services at Good Hope Health Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:26.566+03	2025-09-01 19:59:26.566+03	12330	20
26613	General Medical Services	Basic medical services provided at Raimu Hospital Limited-Malaba	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:28.315+03	2025-09-01 19:59:28.315+03	12331	11
26614	Emergency Response Services	Emergency response services at Raimu Hospital Limited-Malaba	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:28.322+03	2025-09-01 19:59:28.322+03	12331	27
26615	Counseling & Support Services	Counseling and support services at Raimu Hospital Limited-Malaba	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:28.331+03	2025-09-01 19:59:28.331+03	12331	20
26616	General Medical Services	Basic medical services provided at St.James Infirmary Busia Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:29.664+03	2025-09-01 19:59:29.664+03	12332	11
26617	Counseling & Support Services	Counseling and support services at St.James Infirmary Busia Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:29.679+03	2025-09-01 19:59:29.679+03	12332	20
26618	General Medical Services	Basic medical services provided at Oasis Doctors Plaza Busia Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:31.322+03	2025-09-01 19:59:31.322+03	12333	11
26619	Counseling & Support Services	Counseling and support services at Oasis Doctors Plaza Busia Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:31.33+03	2025-09-01 19:59:31.33+03	12333	20
26620	General Medical Services	Basic medical services provided at Blossom Dental Clinic Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:32.997+03	2025-09-01 19:59:32.997+03	12334	11
26621	Counseling & Support Services	Counseling and support services at Blossom Dental Clinic Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:33.005+03	2025-09-01 19:59:33.005+03	12334	20
26622	General Medical Services	Basic medical services provided at Esikoma Community Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:34.377+03	2025-09-01 19:59:34.377+03	12335	11
26623	Emergency Response Services	Emergency response services at Esikoma Community Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:34.384+03	2025-09-01 19:59:34.384+03	12335	27
26624	Counseling & Support Services	Counseling and support services at Esikoma Community Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:34.392+03	2025-09-01 19:59:34.392+03	12335	20
26625	General Medical Services	Basic medical services provided at Alinacare Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:35.722+03	2025-09-01 19:59:35.722+03	12336	11
26626	Counseling & Support Services	Counseling and support services at Alinacare Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:35.73+03	2025-09-01 19:59:35.73+03	12336	20
26627	General Medical Services	Basic medical services provided at Chalondra Healthcare Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:37.043+03	2025-09-01 19:59:37.043+03	12337	11
26628	Counseling & Support Services	Counseling and support services at Chalondra Healthcare Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:37.051+03	2025-09-01 19:59:37.051+03	12337	20
26629	General Medical Services	Basic medical services provided at Bulwani Priv Ate Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:38.628+03	2025-09-01 19:59:38.628+03	12338	11
26630	Emergency Response Services	Emergency response services at Bulwani Priv Ate Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:38.636+03	2025-09-01 19:59:38.636+03	12338	27
26631	Counseling & Support Services	Counseling and support services at Bulwani Priv Ate Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:38.643+03	2025-09-01 19:59:38.643+03	12338	20
26632	General Medical Services	Basic medical services provided at Endo Health Centre Mission	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:40.119+03	2025-09-01 19:59:40.119+03	12339	11
26633	Counseling & Support Services	Counseling and support services at Endo Health Centre Mission	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:40.128+03	2025-09-01 19:59:40.128+03	12339	20
26634	General Medical Services	Basic medical services provided at Embobut Catholic Mission Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:41.405+03	2025-09-01 19:59:41.405+03	12340	11
26635	Counseling & Support Services	Counseling and support services at Embobut Catholic Mission Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:41.412+03	2025-09-01 19:59:41.412+03	12340	20
26636	General Medical Services	Basic medical services provided at Kapkoi Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:42.878+03	2025-09-01 19:59:42.878+03	12341	11
26637	Counseling & Support Services	Counseling and support services at Kapkoi Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:42.884+03	2025-09-01 19:59:42.884+03	12341	20
26638	General Medical Services	Basic medical services provided at Chesongoch Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:42.985+03	2025-09-01 19:59:42.985+03	12342	11
26639	Emergency Response Services	Emergency response services at Chesongoch Mission Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:42.994+03	2025-09-01 19:59:42.994+03	12342	27
26640	Counseling & Support Services	Counseling and support services at Chesongoch Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:43+03	2025-09-01 19:59:43+03	12342	20
26641	General Medical Services	Basic medical services provided at Bliss Healthcare Ltd Iten	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:44.48+03	2025-09-01 19:59:44.48+03	12343	11
26642	Counseling & Support Services	Counseling and support services at Bliss Healthcare Ltd Iten	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:44.488+03	2025-09-01 19:59:44.488+03	12343	20
26643	General Medical Services	Basic medical services provided at Cheptongei Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:45.863+03	2025-09-01 19:59:45.863+03	12344	11
26644	Counseling & Support Services	Counseling and support services at Cheptongei Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:45.869+03	2025-09-01 19:59:45.869+03	12344	20
26645	General Medical Services	Basic medical services provided at Lj Malel Medical Centre Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:47.182+03	2025-09-01 19:59:47.182+03	12345	11
26646	Counseling & Support Services	Counseling and support services at Lj Malel Medical Centre Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:47.19+03	2025-09-01 19:59:47.19+03	12345	20
26647	General Medical Services	Basic medical services provided at Flax Sa V Anis Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:48.312+03	2025-09-01 19:59:48.312+03	12346	11
26648	Counseling & Support Services	Counseling and support services at Flax Sa V Anis Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:48.321+03	2025-09-01 19:59:48.321+03	12346	20
26649	General Medical Services	Basic medical services provided at Invela Health Care Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:49.806+03	2025-09-01 19:59:49.806+03	12347	11
26650	Counseling & Support Services	Counseling and support services at Invela Health Care Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:49.821+03	2025-09-01 19:59:49.821+03	12347	20
26651	General Medical Services	Basic medical services provided at Equity Afia Limited-Iten Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:51.4+03	2025-09-01 19:59:51.4+03	12348	11
26652	Counseling & Support Services	Counseling and support services at Equity Afia Limited-Iten Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:51.415+03	2025-09-01 19:59:51.415+03	12348	20
26653	General Medical Services	Basic medical services provided at St. Augustine Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:52.855+03	2025-09-01 19:59:52.855+03	12349	11
26654	Counseling & Support Services	Counseling and support services at St. Augustine Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:52.871+03	2025-09-01 19:59:52.871+03	12349	20
26655	General Medical Services	Basic medical services provided at St. Anthony Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:54.274+03	2025-09-01 19:59:54.274+03	12350	11
26656	Counseling & Support Services	Counseling and support services at St. Anthony Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:54.289+03	2025-09-01 19:59:54.289+03	12350	20
26657	General Medical Services	Basic medical services provided at St. Nicholas C.F.W Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:55.779+03	2025-09-01 19:59:55.779+03	12351	11
26658	Counseling & Support Services	Counseling and support services at St. Nicholas C.F.W Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:55.788+03	2025-09-01 19:59:55.788+03	12351	20
26659	General Medical Services	Basic medical services provided at Tender Loving Care Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:57.011+03	2025-09-01 19:59:57.011+03	12352	11
26660	Counseling & Support Services	Counseling and support services at Tender Loving Care Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:57.019+03	2025-09-01 19:59:57.019+03	12352	20
26661	General Medical Services	Basic medical services provided at Embu County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:57.114+03	2025-09-01 19:59:57.114+03	12353	11
26662	Emergency Response Services	Emergency response services at Embu County Referral Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 19:59:57.122+03	2025-09-01 19:59:57.122+03	12353	27
26663	Counseling & Support Services	Counseling and support services at Embu County Referral Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:57.129+03	2025-09-01 19:59:57.129+03	12353	20
26664	General Medical Services	Basic medical services provided at University Of Embu Department Of Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:58.464+03	2025-09-01 19:59:58.464+03	12354	11
26665	Counseling & Support Services	Counseling and support services at University Of Embu Department Of Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 19:59:58.471+03	2025-09-01 19:59:58.471+03	12354	20
26666	General Medical Services	Basic medical services provided at Consolata Hospital Kyeni	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:00.223+03	2025-09-01 20:00:00.223+03	12355	11
26667	Emergency Response Services	Emergency response services at Consolata Hospital Kyeni	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:00.232+03	2025-09-01 20:00:00.232+03	12355	27
26668	Counseling & Support Services	Counseling and support services at Consolata Hospital Kyeni	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:00.241+03	2025-09-01 20:00:00.241+03	12355	20
26669	General Medical Services	Basic medical services provided at Geltrude Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:00.338+03	2025-09-01 20:00:00.338+03	12356	11
26670	Counseling & Support Services	Counseling and support services at Geltrude Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:00.35+03	2025-09-01 20:00:00.35+03	12356	20
26671	General Medical Services	Basic medical services provided at Liviero Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:02.049+03	2025-09-01 20:00:02.049+03	12357	11
26672	Counseling & Support Services	Counseling and support services at Liviero Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:02.068+03	2025-09-01 20:00:02.068+03	12357	20
26673	General Medical Services	Basic medical services provided at St. Marys Dispensary Nguviu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:02.184+03	2025-09-01 20:00:02.184+03	12358	11
26674	Counseling & Support Services	Counseling and support services at St. Marys Dispensary Nguviu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:02.19+03	2025-09-01 20:00:02.19+03	12358	20
26675	General Medical Services	Basic medical services provided at Ack Kiriari Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:02.31+03	2025-09-01 20:00:02.31+03	12359	11
26676	Counseling & Support Services	Counseling and support services at Ack Kiriari Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:02.329+03	2025-09-01 20:00:02.329+03	12359	20
26677	General Medical Services	Basic medical services provided at Mother Mazzarello Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:03.489+03	2025-09-01 20:00:03.489+03	12360	11
26678	Counseling & Support Services	Counseling and support services at Mother Mazzarello Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:03.5+03	2025-09-01 20:00:03.5+03	12360	20
26679	General Medical Services	Basic medical services provided at Kevote Catholic Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:04.792+03	2025-09-01 20:00:04.792+03	12361	11
26680	Counseling & Support Services	Counseling and support services at Kevote Catholic Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:04.8+03	2025-09-01 20:00:04.8+03	12361	20
26681	General Medical Services	Basic medical services provided at Joykim Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:04.872+03	2025-09-01 20:00:04.872+03	12362	11
26682	Counseling & Support Services	Counseling and support services at Joykim Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:04.88+03	2025-09-01 20:00:04.88+03	12362	20
26683	General Medical Services	Basic medical services provided at Liberty Maternity And Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:04.951+03	2025-09-01 20:00:04.951+03	12363	11
26684	Counseling & Support Services	Counseling and support services at Liberty Maternity And Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:04.959+03	2025-09-01 20:00:04.959+03	12363	20
26685	General Medical Services	Basic medical services provided at St. Teresa Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:05.042+03	2025-09-01 20:00:05.042+03	12364	11
26686	Counseling & Support Services	Counseling and support services at St. Teresa Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:05.049+03	2025-09-01 20:00:05.049+03	12364	20
26687	General Medical Services	Basic medical services provided at Faith Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:06.267+03	2025-09-01 20:00:06.267+03	12365	11
26688	Counseling & Support Services	Counseling and support services at Faith Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:06.275+03	2025-09-01 20:00:06.275+03	12365	20
26689	General Medical Services	Basic medical services provided at Afya Line Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:07.918+03	2025-09-01 20:00:07.918+03	12366	11
26690	Counseling & Support Services	Counseling and support services at Afya Line Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:07.925+03	2025-09-01 20:00:07.925+03	12366	20
26691	General Medical Services	Basic medical services provided at Joy Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:09.201+03	2025-09-01 20:00:09.201+03	12367	11
26692	Counseling & Support Services	Counseling and support services at Joy Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:09.212+03	2025-09-01 20:00:09.212+03	12367	20
26693	General Medical Services	Basic medical services provided at Patience Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:10.506+03	2025-09-01 20:00:10.506+03	12368	11
26694	Counseling & Support Services	Counseling and support services at Patience Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:10.513+03	2025-09-01 20:00:10.513+03	12368	20
26695	General Medical Services	Basic medical services provided at Mwea Dental Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:11.924+03	2025-09-01 20:00:11.924+03	12369	11
26696	Counseling & Support Services	Counseling and support services at Mwea Dental Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:11.931+03	2025-09-01 20:00:11.931+03	12369	20
26697	General Medical Services	Basic medical services provided at County Medical Centre Embu Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:12.012+03	2025-09-01 20:00:12.012+03	12370	11
26698	Counseling & Support Services	Counseling and support services at County Medical Centre Embu Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:12.02+03	2025-09-01 20:00:12.02+03	12370	20
26699	General Medical Services	Basic medical services provided at Embu Childrens Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:12.099+03	2025-09-01 20:00:12.099+03	12371	11
26700	Counseling & Support Services	Counseling and support services at Embu Childrens Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:12.107+03	2025-09-01 20:00:12.107+03	12371	20
26701	General Medical Services	Basic medical services provided at Jetma Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:13.541+03	2025-09-01 20:00:13.541+03	12372	11
26702	Counseling & Support Services	Counseling and support services at Jetma Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:13.551+03	2025-09-01 20:00:13.551+03	12372	20
26703	General Medical Services	Basic medical services provided at Promise Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:13.664+03	2025-09-01 20:00:13.664+03	12373	11
26704	Counseling & Support Services	Counseling and support services at Promise Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:13.674+03	2025-09-01 20:00:13.674+03	12373	20
26705	General Medical Services	Basic medical services provided at Cfw Mbuvore Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:14.855+03	2025-09-01 20:00:14.855+03	12374	11
26706	Counseling & Support Services	Counseling and support services at Cfw Mbuvore Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:14.862+03	2025-09-01 20:00:14.862+03	12374	20
26707	General Medical Services	Basic medical services provided at Kimangaru Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:16.067+03	2025-09-01 20:00:16.067+03	12375	11
26708	Counseling & Support Services	Counseling and support services at Kimangaru Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:16.076+03	2025-09-01 20:00:16.076+03	12375	20
26709	General Medical Services	Basic medical services provided at The Aga Khan University Hospital Embu Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:17.317+03	2025-09-01 20:00:17.317+03	12376	11
26710	Emergency Response Services	Emergency response services at The Aga Khan University Hospital Embu Clinic	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:17.327+03	2025-09-01 20:00:17.327+03	12376	27
26711	Counseling & Support Services	Counseling and support services at The Aga Khan University Hospital Embu Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:17.339+03	2025-09-01 20:00:17.339+03	12376	20
26712	General Medical Services	Basic medical services provided at Ka Vutiri Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:17.417+03	2025-09-01 20:00:17.417+03	12377	11
26713	Counseling & Support Services	Counseling and support services at Ka Vutiri Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:17.423+03	2025-09-01 20:00:17.423+03	12377	20
26714	General Medical Services	Basic medical services provided at Huruma Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:18.815+03	2025-09-01 20:00:18.815+03	12378	11
26715	Counseling & Support Services	Counseling and support services at Huruma Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:18.822+03	2025-09-01 20:00:18.822+03	12378	20
26716	General Medical Services	Basic medical services provided at Focus Clinical And Diagnostic Centre Ltd Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:19.969+03	2025-09-01 20:00:19.969+03	12379	11
26717	Counseling & Support Services	Counseling and support services at Focus Clinical And Diagnostic Centre Ltd Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:19.978+03	2025-09-01 20:00:19.978+03	12379	20
26718	General Medical Services	Basic medical services provided at Utugi Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:21.568+03	2025-09-01 20:00:21.568+03	12380	11
26719	Counseling & Support Services	Counseling and support services at Utugi Cfw Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:21.579+03	2025-09-01 20:00:21.579+03	12380	20
26720	General Medical Services	Basic medical services provided at Kings Care Medical Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:23.017+03	2025-09-01 20:00:23.017+03	12381	11
26721	Counseling & Support Services	Counseling and support services at Kings Care Medical Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:23.026+03	2025-09-01 20:00:23.026+03	12381	20
26722	General Medical Services	Basic medical services provided at Yunasi Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:24.427+03	2025-09-01 20:00:24.427+03	12382	11
26723	Counseling & Support Services	Counseling and support services at Yunasi Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:24.434+03	2025-09-01 20:00:24.434+03	12382	20
26724	General Medical Services	Basic medical services provided at Outspan Hospital Embu Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:25.719+03	2025-09-01 20:00:25.719+03	12383	11
26725	Emergency Response Services	Emergency response services at Outspan Hospital Embu Medical Clinic	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:25.727+03	2025-09-01 20:00:25.727+03	12383	27
26726	Counseling & Support Services	Counseling and support services at Outspan Hospital Embu Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:25.743+03	2025-09-01 20:00:25.743+03	12383	20
26727	General Medical Services	Basic medical services provided at Eastend Dental Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:27.136+03	2025-09-01 20:00:27.136+03	12384	11
26728	Counseling & Support Services	Counseling and support services at Eastend Dental Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:27.144+03	2025-09-01 20:00:27.144+03	12384	20
26729	General Medical Services	Basic medical services provided at Potters Family Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:27.294+03	2025-09-01 20:00:27.294+03	12385	11
26730	Emergency Response Services	Emergency response services at Potters Family Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:27.302+03	2025-09-01 20:00:27.302+03	12385	27
26731	Counseling & Support Services	Counseling and support services at Potters Family Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:27.31+03	2025-09-01 20:00:27.31+03	12385	20
26732	General Medical Services	Basic medical services provided at Greenspan Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:28.554+03	2025-09-01 20:00:28.554+03	12386	11
26733	Counseling & Support Services	Counseling and support services at Greenspan Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:28.562+03	2025-09-01 20:00:28.562+03	12386	20
26734	General Medical Services	Basic medical services provided at Optident Dental Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:29.845+03	2025-09-01 20:00:29.845+03	12387	11
26735	Counseling & Support Services	Counseling and support services at Optident Dental Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:29.857+03	2025-09-01 20:00:29.857+03	12387	20
26736	General Medical Services	Basic medical services provided at Makutano Family Healthcare Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:30.98+03	2025-09-01 20:00:30.98+03	12388	11
26737	Counseling & Support Services	Counseling and support services at Makutano Family Healthcare Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:30.989+03	2025-09-01 20:00:30.989+03	12388	20
26738	General Medical Services	Basic medical services provided at Kirimara Opticals Ltd Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:32.464+03	2025-09-01 20:00:32.464+03	12389	11
26739	Counseling & Support Services	Counseling and support services at Kirimara Opticals Ltd Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:32.473+03	2025-09-01 20:00:32.473+03	12389	20
26740	General Medical Services	Basic medical services provided at Daima Medical Clinic-Dallas	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:33.873+03	2025-09-01 20:00:33.873+03	12390	11
26741	Counseling & Support Services	Counseling and support services at Daima Medical Clinic-Dallas	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:33.894+03	2025-09-01 20:00:33.894+03	12390	20
26742	General Medical Services	Basic medical services provided at Odicare Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:35.472+03	2025-09-01 20:00:35.472+03	12391	11
26743	Counseling & Support Services	Counseling and support services at Odicare Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:35.483+03	2025-09-01 20:00:35.483+03	12391	20
26744	General Medical Services	Basic medical services provided at Angel Care Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:37.005+03	2025-09-01 20:00:37.005+03	12392	11
26745	Counseling & Support Services	Counseling and support services at Angel Care Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:37.012+03	2025-09-01 20:00:37.012+03	12392	20
26746	General Medical Services	Basic medical services provided at Embu Tumaini Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:38.215+03	2025-09-01 20:00:38.215+03	12393	11
26747	Counseling & Support Services	Counseling and support services at Embu Tumaini Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:38.223+03	2025-09-01 20:00:38.223+03	12393	20
26748	General Medical Services	Basic medical services provided at Elimundani Health Care Kiritiri	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:39.563+03	2025-09-01 20:00:39.563+03	12394	11
26749	Counseling & Support Services	Counseling and support services at Elimundani Health Care Kiritiri	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:39.573+03	2025-09-01 20:00:39.573+03	12394	20
26750	General Medical Services	Basic medical services provided at Embu Children Hospital Tenri Makima	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:41.115+03	2025-09-01 20:00:41.115+03	12395	11
26751	Emergency Response Services	Emergency response services at Embu Children Hospital Tenri Makima	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:41.121+03	2025-09-01 20:00:41.121+03	12395	27
26752	Counseling & Support Services	Counseling and support services at Embu Children Hospital Tenri Makima	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:41.128+03	2025-09-01 20:00:41.128+03	12395	20
26753	General Medical Services	Basic medical services provided at Smart Smile Dental Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:42.617+03	2025-09-01 20:00:42.617+03	12396	11
26754	Counseling & Support Services	Counseling and support services at Smart Smile Dental Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:42.624+03	2025-09-01 20:00:42.624+03	12396	20
26755	General Medical Services	Basic medical services provided at Embu Medical And Dental Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:43.95+03	2025-09-01 20:00:43.95+03	12397	11
26756	Counseling & Support Services	Counseling and support services at Embu Medical And Dental Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:43.957+03	2025-09-01 20:00:43.957+03	12397	20
26757	General Medical Services	Basic medical services provided at Imara Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:45.245+03	2025-09-01 20:00:45.245+03	12398	11
26758	Emergency Response Services	Emergency response services at Imara Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:45.254+03	2025-09-01 20:00:45.254+03	12398	27
26759	Counseling & Support Services	Counseling and support services at Imara Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:45.268+03	2025-09-01 20:00:45.268+03	12398	20
26760	General Medical Services	Basic medical services provided at Shanwes Med Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:45.347+03	2025-09-01 20:00:45.347+03	12399	11
26761	Counseling & Support Services	Counseling and support services at Shanwes Med Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:45.353+03	2025-09-01 20:00:45.353+03	12399	20
26762	General Medical Services	Basic medical services provided at Mt Kenya Heart And Diabetes Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:46.665+03	2025-09-01 20:00:46.665+03	12400	11
26763	Counseling & Support Services	Counseling and support services at Mt Kenya Heart And Diabetes Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:46.683+03	2025-09-01 20:00:46.683+03	12400	20
26764	General Medical Services	Basic medical services provided at Visionners Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:48.573+03	2025-09-01 20:00:48.573+03	12401	11
26765	Counseling & Support Services	Counseling and support services at Visionners Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:48.589+03	2025-09-01 20:00:48.589+03	12401	20
26766	General Medical Services	Basic medical services provided at Murithi Metho Optometrist	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:50.476+03	2025-09-01 20:00:50.476+03	12402	11
26767	Counseling & Support Services	Counseling and support services at Murithi Metho Optometrist	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:50.487+03	2025-09-01 20:00:50.487+03	12402	20
26768	General Medical Services	Basic medical services provided at Pure Medcare Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:52.129+03	2025-09-01 20:00:52.129+03	12403	11
26769	Counseling & Support Services	Counseling and support services at Pure Medcare Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:52.144+03	2025-09-01 20:00:52.144+03	12403	20
26770	General Medical Services	Basic medical services provided at Kianjokoma Muungano Community Cottage Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:53.569+03	2025-09-01 20:00:53.569+03	12404	11
26771	Emergency Response Services	Emergency response services at Kianjokoma Muungano Community Cottage Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:53.577+03	2025-09-01 20:00:53.577+03	12404	27
26772	Counseling & Support Services	Counseling and support services at Kianjokoma Muungano Community Cottage Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:53.596+03	2025-09-01 20:00:53.596+03	12404	20
26773	General Medical Services	Basic medical services provided at Frev Ane Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:55.479+03	2025-09-01 20:00:55.479+03	12405	11
26774	Emergency Response Services	Emergency response services at Frev Ane Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:00:55.497+03	2025-09-01 20:00:55.497+03	12405	27
26775	Counseling & Support Services	Counseling and support services at Frev Ane Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:55.518+03	2025-09-01 20:00:55.518+03	12405	20
26776	General Medical Services	Basic medical services provided at Mercy Medical Clinic-Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:56.804+03	2025-09-01 20:00:56.804+03	12406	11
26777	Counseling & Support Services	Counseling and support services at Mercy Medical Clinic-Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:56.813+03	2025-09-01 20:00:56.813+03	12406	20
26778	General Medical Services	Basic medical services provided at St. Jude Medical Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:56.917+03	2025-09-01 20:00:56.917+03	12407	11
26779	Counseling & Support Services	Counseling and support services at St. Jude Medical Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:56.928+03	2025-09-01 20:00:56.928+03	12407	20
26780	General Medical Services	Basic medical services provided at Generation And Visionary Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:57.064+03	2025-09-01 20:00:57.064+03	12408	11
26781	Counseling & Support Services	Counseling and support services at Generation And Visionary Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:57.071+03	2025-09-01 20:00:57.071+03	12408	20
26782	General Medical Services	Basic medical services provided at Mount Hermon Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:59.171+03	2025-09-01 20:00:59.171+03	12409	11
26783	Counseling & Support Services	Counseling and support services at Mount Hermon Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:00:59.188+03	2025-09-01 20:00:59.188+03	12409	20
26784	General Medical Services	Basic medical services provided at Mariari Ebenzer Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:00.972+03	2025-09-01 20:01:00.972+03	12410	11
26785	Counseling & Support Services	Counseling and support services at Mariari Ebenzer Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:00.982+03	2025-09-01 20:01:00.982+03	12410	20
26786	General Medical Services	Basic medical services provided at Amaze Dental Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:02.528+03	2025-09-01 20:01:02.528+03	12411	11
26787	Counseling & Support Services	Counseling and support services at Amaze Dental Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:02.535+03	2025-09-01 20:01:02.535+03	12411	20
26788	General Medical Services	Basic medical services provided at Highrise Health Care Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:04.073+03	2025-09-01 20:01:04.073+03	12412	11
26789	Counseling & Support Services	Counseling and support services at Highrise Health Care Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:04.082+03	2025-09-01 20:01:04.082+03	12412	20
26790	General Medical Services	Basic medical services provided at Greensprings Medical Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:05.601+03	2025-09-01 20:01:05.601+03	12413	11
26791	Counseling & Support Services	Counseling and support services at Greensprings Medical Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:05.61+03	2025-09-01 20:01:05.61+03	12413	20
26792	General Medical Services	Basic medical services provided at Royal Smiles Dental Clinic Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:07.391+03	2025-09-01 20:01:07.391+03	12414	11
26793	Counseling & Support Services	Counseling and support services at Royal Smiles Dental Clinic Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:07.397+03	2025-09-01 20:01:07.397+03	12414	20
26794	General Medical Services	Basic medical services provided at Granton  Dolly Nursing Home Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:08.814+03	2025-09-01 20:01:08.814+03	12415	11
26795	Counseling & Support Services	Counseling and support services at Granton  Dolly Nursing Home Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:08.822+03	2025-09-01 20:01:08.822+03	12415	20
26796	General Medical Services	Basic medical services provided at Kiambere Medical Healthcare Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:10.248+03	2025-09-01 20:01:10.248+03	12416	11
26797	Counseling & Support Services	Counseling and support services at Kiambere Medical Healthcare Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:10.255+03	2025-09-01 20:01:10.255+03	12416	20
26798	General Medical Services	Basic medical services provided at Nairobi Radiotherapy  Cancer Centre Limited-Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:12.304+03	2025-09-01 20:01:12.304+03	12417	11
26799	Counseling & Support Services	Counseling and support services at Nairobi Radiotherapy  Cancer Centre Limited-Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:12.313+03	2025-09-01 20:01:12.313+03	12417	20
26800	General Medical Services	Basic medical services provided at Patocare Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:13.969+03	2025-09-01 20:01:13.969+03	12418	11
26801	Counseling & Support Services	Counseling and support services at Patocare Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:13.978+03	2025-09-01 20:01:13.978+03	12418	20
26802	General Medical Services	Basic medical services provided at V Alley View Medical Specialist And Diagnostic Embu Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:15.346+03	2025-09-01 20:01:15.346+03	12419	11
26803	Counseling & Support Services	Counseling and support services at V Alley View Medical Specialist And Diagnostic Embu Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:15.361+03	2025-09-01 20:01:15.361+03	12419	20
26804	General Medical Services	Basic medical services provided at Tumaini Medical Centre Rwika	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:17.308+03	2025-09-01 20:01:17.308+03	12420	11
26805	Counseling & Support Services	Counseling and support services at Tumaini Medical Centre Rwika	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:17.32+03	2025-09-01 20:01:17.32+03	12420	20
26806	General Medical Services	Basic medical services provided at Mbuvori Prime Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:18.798+03	2025-09-01 20:01:18.798+03	12421	11
26807	Counseling & Support Services	Counseling and support services at Mbuvori Prime Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:18.805+03	2025-09-01 20:01:18.805+03	12421	20
26808	General Medical Services	Basic medical services provided at Marini-Medical Centre Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:20.598+03	2025-09-01 20:01:20.598+03	12422	11
26809	Counseling & Support Services	Counseling and support services at Marini-Medical Centre Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:20.605+03	2025-09-01 20:01:20.605+03	12422	20
26810	General Medical Services	Basic medical services provided at Cynerd Healthcare Group Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:22.046+03	2025-09-01 20:01:22.046+03	12423	11
26811	Counseling & Support Services	Counseling and support services at Cynerd Healthcare Group Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:22.058+03	2025-09-01 20:01:22.058+03	12423	20
26812	General Medical Services	Basic medical services provided at Magnificent Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:23.651+03	2025-09-01 20:01:23.651+03	12424	11
26813	Counseling & Support Services	Counseling and support services at Magnificent Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:23.658+03	2025-09-01 20:01:23.658+03	12424	20
26814	General Medical Services	Basic medical services provided at Serenity Homes Rehabilitation And Counselling Center Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:24.88+03	2025-09-01 20:01:24.88+03	12425	11
26815	Counseling & Support Services	Counseling and support services at Serenity Homes Rehabilitation And Counselling Center Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:24.887+03	2025-09-01 20:01:24.887+03	12425	20
26816	General Medical Services	Basic medical services provided at Pleroma Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:26.733+03	2025-09-01 20:01:26.733+03	12426	11
26817	Counseling & Support Services	Counseling and support services at Pleroma Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:26.739+03	2025-09-01 20:01:26.739+03	12426	20
26818	General Medical Services	Basic medical services provided at Vicoptic Eyeclinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:28.136+03	2025-09-01 20:01:28.136+03	12427	11
26819	Counseling & Support Services	Counseling and support services at Vicoptic Eyeclinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:28.143+03	2025-09-01 20:01:28.143+03	12427	20
26820	General Medical Services	Basic medical services provided at Imara Hospital Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:29.617+03	2025-09-01 20:01:29.617+03	12428	11
26821	Emergency Response Services	Emergency response services at Imara Hospital Embu	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:01:29.624+03	2025-09-01 20:01:29.624+03	12428	27
26822	Counseling & Support Services	Counseling and support services at Imara Hospital Embu	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:29.633+03	2025-09-01 20:01:29.633+03	12428	20
26823	General Medical Services	Basic medical services provided at Loyalty Hope Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:30.821+03	2025-09-01 20:01:30.821+03	12429	11
26824	Counseling & Support Services	Counseling and support services at Loyalty Hope Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:30.831+03	2025-09-01 20:01:30.831+03	12429	20
26825	General Medical Services	Basic medical services provided at Njukiri Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:32.019+03	2025-09-01 20:01:32.019+03	12430	11
26826	Counseling & Support Services	Counseling and support services at Njukiri Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:32.026+03	2025-09-01 20:01:32.026+03	12430	20
26827	General Medical Services	Basic medical services provided at Embu Premier Physicians Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:33.161+03	2025-09-01 20:01:33.161+03	12431	11
26828	Counseling & Support Services	Counseling and support services at Embu Premier Physicians Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:33.171+03	2025-09-01 20:01:33.171+03	12431	20
26829	General Medical Services	Basic medical services provided at The Paradox Hospitals	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:34.822+03	2025-09-01 20:01:34.822+03	12432	11
26830	Emergency Response Services	Emergency response services at The Paradox Hospitals	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:01:34.832+03	2025-09-01 20:01:34.832+03	12432	27
26831	Counseling & Support Services	Counseling and support services at The Paradox Hospitals	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:34.839+03	2025-09-01 20:01:34.839+03	12432	20
26832	General Medical Services	Basic medical services provided at Kiritiri Funeral Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:36.563+03	2025-09-01 20:01:36.563+03	12433	11
26833	Counseling & Support Services	Counseling and support services at Kiritiri Funeral Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:36.575+03	2025-09-01 20:01:36.575+03	12433	20
26834	General Medical Services	Basic medical services provided at Forealtors Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:38.041+03	2025-09-01 20:01:38.041+03	12434	11
26835	Emergency Response Services	Emergency response services at Forealtors Hospital Ltd	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:01:38.048+03	2025-09-01 20:01:38.048+03	12434	27
26836	Counseling & Support Services	Counseling and support services at Forealtors Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:38.062+03	2025-09-01 20:01:38.062+03	12434	20
26837	General Medical Services	Basic medical services provided at Walter Medical And Dental Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:39.452+03	2025-09-01 20:01:39.452+03	12435	11
26838	Counseling & Support Services	Counseling and support services at Walter Medical And Dental Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:39.47+03	2025-09-01 20:01:39.47+03	12435	20
26839	General Medical Services	Basic medical services provided at Framary Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:40.769+03	2025-09-01 20:01:40.769+03	12436	11
26840	Counseling & Support Services	Counseling and support services at Framary Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:40.778+03	2025-09-01 20:01:40.778+03	12436	20
26841	General Medical Services	Basic medical services provided at Ericare Medical And Physiotherapy Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:42.046+03	2025-09-01 20:01:42.046+03	12437	11
26842	Counseling & Support Services	Counseling and support services at Ericare Medical And Physiotherapy Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:42.055+03	2025-09-01 20:01:42.056+03	12437	20
26843	General Medical Services	Basic medical services provided at Emmanuel Meka Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:43.43+03	2025-09-01 20:01:43.43+03	12438	11
26844	Counseling & Support Services	Counseling and support services at Emmanuel Meka Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:43.437+03	2025-09-01 20:01:43.437+03	12438	20
26845	General Medical Services	Basic medical services provided at Neema Universal Health Care Limited-Embu Town	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:45.248+03	2025-09-01 20:01:45.248+03	12439	11
26846	Counseling & Support Services	Counseling and support services at Neema Universal Health Care Limited-Embu Town	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:45.256+03	2025-09-01 20:01:45.256+03	12439	20
26847	General Medical Services	Basic medical services provided at Fountain Of Hope Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:46.932+03	2025-09-01 20:01:46.932+03	12440	11
26848	Counseling & Support Services	Counseling and support services at Fountain Of Hope Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:46.941+03	2025-09-01 20:01:46.941+03	12440	20
26849	General Medical Services	Basic medical services provided at Kamiu Junction Community Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:47.041+03	2025-09-01 20:01:47.041+03	12441	11
26850	Counseling & Support Services	Counseling and support services at Kamiu Junction Community Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:47.049+03	2025-09-01 20:01:47.049+03	12441	20
26851	General Medical Services	Basic medical services provided at Graceview Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:48.532+03	2025-09-01 20:01:48.532+03	12442	11
26852	Counseling & Support Services	Counseling and support services at Graceview Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:48.539+03	2025-09-01 20:01:48.539+03	12442	20
26853	General Medical Services	Basic medical services provided at Kengen Gitaru Staff Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:49.871+03	2025-09-01 20:01:49.871+03	12443	11
26854	Counseling & Support Services	Counseling and support services at Kengen Gitaru Staff Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:49.881+03	2025-09-01 20:01:49.881+03	12443	20
26855	General Medical Services	Basic medical services provided at Garissa Mother And Child Health Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:51.345+03	2025-09-01 20:01:51.345+03	12444	11
26856	Counseling & Support Services	Counseling and support services at Garissa Mother And Child Health Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:51.353+03	2025-09-01 20:01:51.353+03	12444	20
26857	General Medical Services	Basic medical services provided at Towba Medical Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:52.917+03	2025-09-01 20:01:52.917+03	12445	11
26858	Counseling & Support Services	Counseling and support services at Towba Medical Care	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:52.927+03	2025-09-01 20:01:52.927+03	12445	20
26859	General Medical Services	Basic medical services provided at Bulla Hagar Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:54.137+03	2025-09-01 20:01:54.137+03	12446	11
26860	Counseling & Support Services	Counseling and support services at Bulla Hagar Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:54.145+03	2025-09-01 20:01:54.145+03	12446	20
26861	General Medical Services	Basic medical services provided at Iom Migration Assesment Centre Dadaab	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:54.258+03	2025-09-01 20:01:54.258+03	12447	11
26862	Counseling & Support Services	Counseling and support services at Iom Migration Assesment Centre Dadaab	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:54.265+03	2025-09-01 20:01:54.265+03	12447	20
26863	General Medical Services	Basic medical services provided at Garissa Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:56.15+03	2025-09-01 20:01:56.15+03	12448	11
26864	Counseling & Support Services	Counseling and support services at Garissa Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:56.158+03	2025-09-01 20:01:56.158+03	12448	20
26865	General Medical Services	Basic medical services provided at Simaho Mchfp Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:56.365+03	2025-09-01 20:01:56.365+03	12449	11
26866	Counseling & Support Services	Counseling and support services at Simaho Mchfp Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:56.374+03	2025-09-01 20:01:56.374+03	12449	20
26867	General Medical Services	Basic medical services provided at Noorhilac Pharmaceutical Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:57.809+03	2025-09-01 20:01:57.809+03	12450	11
26868	Counseling & Support Services	Counseling and support services at Noorhilac Pharmaceutical Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:57.816+03	2025-09-01 20:01:57.816+03	12450	20
26869	General Medical Services	Basic medical services provided at Excel Health Services Garissa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:59.255+03	2025-09-01 20:01:59.255+03	12451	11
26870	Counseling & Support Services	Counseling and support services at Excel Health Services Garissa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:01:59.263+03	2025-09-01 20:01:59.263+03	12451	20
26871	General Medical Services	Basic medical services provided at Medina Medicare Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:00.909+03	2025-09-01 20:02:00.909+03	12452	11
26872	Emergency Response Services	Emergency response services at Medina Medicare Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:00.916+03	2025-09-01 20:02:00.916+03	12452	27
26873	Counseling & Support Services	Counseling and support services at Medina Medicare Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:00.924+03	2025-09-01 20:02:00.924+03	12452	20
26874	General Medical Services	Basic medical services provided at Tawheed Community Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:02.693+03	2025-09-01 20:02:02.693+03	12453	11
26875	Counseling & Support Services	Counseling and support services at Tawheed Community Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:02.705+03	2025-09-01 20:02:02.705+03	12453	20
26876	General Medical Services	Basic medical services provided at North Eastern Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:04.011+03	2025-09-01 20:02:04.011+03	12454	11
26877	Counseling & Support Services	Counseling and support services at North Eastern Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:04.02+03	2025-09-01 20:02:04.02+03	12454	20
26878	General Medical Services	Basic medical services provided at Medina Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:05.216+03	2025-09-01 20:02:05.216+03	12455	11
26879	Emergency Response Services	Emergency response services at Medina Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:05.234+03	2025-09-01 20:02:05.234+03	12455	27
26880	Counseling & Support Services	Counseling and support services at Medina Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:05.252+03	2025-09-01 20:02:05.252+03	12455	20
26881	General Medical Services	Basic medical services provided at Womens Initiative Health Care Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:05.412+03	2025-09-01 20:02:05.412+03	12456	11
26882	Counseling & Support Services	Counseling and support services at Womens Initiative Health Care Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:05.428+03	2025-09-01 20:02:05.428+03	12456	20
26883	General Medical Services	Basic medical services provided at Alliance Medical Centre Ltd Garissa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:07.075+03	2025-09-01 20:02:07.075+03	12457	11
26884	Counseling & Support Services	Counseling and support services at Alliance Medical Centre Ltd Garissa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:07.083+03	2025-09-01 20:02:07.083+03	12457	20
26885	General Medical Services	Basic medical services provided at Cosgurow Healthcare Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:08.66+03	2025-09-01 20:02:08.66+03	12458	11
26886	Counseling & Support Services	Counseling and support services at Cosgurow Healthcare Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:08.685+03	2025-09-01 20:02:08.685+03	12458	20
26887	General Medical Services	Basic medical services provided at Al-Maqdis Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:10.002+03	2025-09-01 20:02:10.002+03	12459	11
26888	Counseling & Support Services	Counseling and support services at Al-Maqdis Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:10.011+03	2025-09-01 20:02:10.011+03	12459	20
26889	General Medical Services	Basic medical services provided at Al Amin Medical  Labaratory	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:11.104+03	2025-09-01 20:02:11.104+03	12460	11
26890	Counseling & Support Services	Counseling and support services at Al Amin Medical  Labaratory	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:11.112+03	2025-09-01 20:02:11.112+03	12460	20
26891	General Medical Services	Basic medical services provided at Garissa Childrens Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:12.544+03	2025-09-01 20:02:12.544+03	12461	11
26892	Emergency Response Services	Emergency response services at Garissa Childrens Hospital Ltd	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:12.551+03	2025-09-01 20:02:12.552+03	12461	27
26893	Counseling & Support Services	Counseling and support services at Garissa Childrens Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:12.56+03	2025-09-01 20:02:12.56+03	12461	20
26894	General Medical Services	Basic medical services provided at Count Medical And Diagnostic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:14.41+03	2025-09-01 20:02:14.41+03	12462	11
26895	Counseling & Support Services	Counseling and support services at Count Medical And Diagnostic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:14.42+03	2025-09-01 20:02:14.42+03	12462	20
26896	General Medical Services	Basic medical services provided at Zensturion Community Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:15.812+03	2025-09-01 20:02:15.814+03	12463	11
26897	Counseling & Support Services	Counseling and support services at Zensturion Community Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:15.821+03	2025-09-01 20:02:15.821+03	12463	20
26898	General Medical Services	Basic medical services provided at Afnaan Healthcare Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:17.631+03	2025-09-01 20:02:17.631+03	12464	11
26899	Counseling & Support Services	Counseling and support services at Afnaan Healthcare Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:17.639+03	2025-09-01 20:02:17.639+03	12464	20
26900	General Medical Services	Basic medical services provided at Hilwa Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:19.008+03	2025-09-01 20:02:19.008+03	12465	11
26901	Counseling & Support Services	Counseling and support services at Hilwa Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:19.016+03	2025-09-01 20:02:19.016+03	12465	20
26902	General Medical Services	Basic medical services provided at Al -Bushra Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:19.094+03	2025-09-01 20:02:19.094+03	12466	11
26903	Counseling & Support Services	Counseling and support services at Al -Bushra Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:19.101+03	2025-09-01 20:02:19.101+03	12466	20
26904	General Medical Services	Basic medical services provided at Medina Medicare Hospital Limited-Hagardera	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:19.194+03	2025-09-01 20:02:19.194+03	12467	11
26905	Emergency Response Services	Emergency response services at Medina Medicare Hospital Limited-Hagardera	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:19.201+03	2025-09-01 20:02:19.201+03	12467	27
26906	Counseling & Support Services	Counseling and support services at Medina Medicare Hospital Limited-Hagardera	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:19.208+03	2025-09-01 20:02:19.208+03	12467	20
26907	General Medical Services	Basic medical services provided at Familyfirst Medical Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:20.868+03	2025-09-01 20:02:20.868+03	12468	11
26908	Counseling & Support Services	Counseling and support services at Familyfirst Medical Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:20.889+03	2025-09-01 20:02:20.889+03	12468	20
26909	General Medical Services	Basic medical services provided at Northgate Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:22.058+03	2025-09-01 20:02:22.058+03	12469	11
26910	Emergency Response Services	Emergency response services at Northgate Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:22.066+03	2025-09-01 20:02:22.066+03	12469	27
26911	Counseling & Support Services	Counseling and support services at Northgate Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:22.073+03	2025-09-01 20:02:22.073+03	12469	20
26912	General Medical Services	Basic medical services provided at Jihan Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:23.231+03	2025-09-01 20:02:23.232+03	12470	11
26913	Counseling & Support Services	Counseling and support services at Jihan Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:23.24+03	2025-09-01 20:02:23.24+03	12470	20
26914	General Medical Services	Basic medical services provided at Garissa Doctors Plaza	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:24.267+03	2025-09-01 20:02:24.267+03	12471	11
26915	Counseling & Support Services	Counseling and support services at Garissa Doctors Plaza	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:24.274+03	2025-09-01 20:02:24.274+03	12471	20
26916	General Medical Services	Basic medical services provided at Tasneem Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:25.876+03	2025-09-01 20:02:25.876+03	12472	11
26917	Counseling & Support Services	Counseling and support services at Tasneem Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:25.89+03	2025-09-01 20:02:25.89+03	12472	20
26918	General Medical Services	Basic medical services provided at Al-Rashad Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:27.195+03	2025-09-01 20:02:27.195+03	12473	11
26919	Counseling & Support Services	Counseling and support services at Al-Rashad Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:27.203+03	2025-09-01 20:02:27.203+03	12473	20
26920	General Medical Services	Basic medical services provided at Sunna Healthcare  Dental Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:28.44+03	2025-09-01 20:02:28.44+03	12474	11
26921	Counseling & Support Services	Counseling and support services at Sunna Healthcare  Dental Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:28.45+03	2025-09-01 20:02:28.45+03	12474	20
26922	General Medical Services	Basic medical services provided at Ankara Medical Center Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:29.756+03	2025-09-01 20:02:29.756+03	12475	11
26923	Counseling & Support Services	Counseling and support services at Ankara Medical Center Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:29.762+03	2025-09-01 20:02:29.762+03	12475	20
26924	General Medical Services	Basic medical services provided at Garissa Ent Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:31.411+03	2025-09-01 20:02:31.411+03	12476	11
26925	Counseling & Support Services	Counseling and support services at Garissa Ent Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:31.442+03	2025-09-01 20:02:31.442+03	12476	20
26926	General Medical Services	Basic medical services provided at Anfac Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:32.648+03	2025-09-01 20:02:32.648+03	12477	11
26927	Counseling & Support Services	Counseling and support services at Anfac Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:32.656+03	2025-09-01 20:02:32.656+03	12477	20
26928	General Medical Services	Basic medical services provided at Masalani Diagnostic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:33.778+03	2025-09-01 20:02:33.778+03	12478	11
26929	Counseling & Support Services	Counseling and support services at Masalani Diagnostic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:33.786+03	2025-09-01 20:02:33.786+03	12478	20
26930	General Medical Services	Basic medical services provided at Al-Qudus Medical Centre Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:35.149+03	2025-09-01 20:02:35.149+03	12479	11
26931	Counseling & Support Services	Counseling and support services at Al-Qudus Medical Centre Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:35.156+03	2025-09-01 20:02:35.156+03	12479	20
26932	General Medical Services	Basic medical services provided at Madogashe Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:35.241+03	2025-09-01 20:02:35.241+03	12480	11
26933	Counseling & Support Services	Counseling and support services at Madogashe Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:35.249+03	2025-09-01 20:02:35.249+03	12480	20
26934	General Medical Services	Basic medical services provided at Modogashe Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:36.771+03	2025-09-01 20:02:36.771+03	12481	11
26935	Counseling & Support Services	Counseling and support services at Modogashe Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:36.797+03	2025-09-01 20:02:36.797+03	12481	20
26936	General Medical Services	Basic medical services provided at Garissa Nursing Home Annex	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:36.893+03	2025-09-01 20:02:36.893+03	12482	11
26937	Counseling & Support Services	Counseling and support services at Garissa Nursing Home Annex	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:36.9+03	2025-09-01 20:02:36.9+03	12482	20
26938	General Medical Services	Basic medical services provided at Antaliya Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:38.137+03	2025-09-01 20:02:38.137+03	12483	11
26939	Emergency Response Services	Emergency response services at Antaliya Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:38.145+03	2025-09-01 20:02:38.145+03	12483	27
26940	Counseling & Support Services	Counseling and support services at Antaliya Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:38.152+03	2025-09-01 20:02:38.152+03	12483	20
26941	General Medical Services	Basic medical services provided at Dagahley Medical Health Care Services Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:39.339+03	2025-09-01 20:02:39.339+03	12484	11
26942	Counseling & Support Services	Counseling and support services at Dagahley Medical Health Care Services Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:39.348+03	2025-09-01 20:02:39.348+03	12484	20
26943	General Medical Services	Basic medical services provided at Highgate Healthcare Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:40.723+03	2025-09-01 20:02:40.723+03	12485	11
26944	Counseling & Support Services	Counseling and support services at Highgate Healthcare Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:40.731+03	2025-09-01 20:02:40.731+03	12485	20
26945	General Medical Services	Basic medical services provided at Sarap Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:42.531+03	2025-09-01 20:02:42.531+03	12486	11
26946	Counseling & Support Services	Counseling and support services at Sarap Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:42.538+03	2025-09-01 20:02:42.538+03	12486	20
26947	General Medical Services	Basic medical services provided at Garissa Eye Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:43.592+03	2025-09-01 20:02:43.592+03	12487	11
26948	Emergency Response Services	Emergency response services at Garissa Eye Hospital Ltd	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:43.6+03	2025-09-01 20:02:43.6+03	12487	27
26949	Counseling & Support Services	Counseling and support services at Garissa Eye Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:43.608+03	2025-09-01 20:02:43.608+03	12487	20
26950	General Medical Services	Basic medical services provided at Jamia Islamic Intergrated Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:44.835+03	2025-09-01 20:02:44.835+03	12488	11
26951	Counseling & Support Services	Counseling and support services at Jamia Islamic Intergrated Health Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:44.849+03	2025-09-01 20:02:44.849+03	12488	20
26952	General Medical Services	Basic medical services provided at Hamdan Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:46.35+03	2025-09-01 20:02:46.35+03	12489	11
26953	Counseling & Support Services	Counseling and support services at Hamdan Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:46.363+03	2025-09-01 20:02:46.363+03	12489	20
26954	General Medical Services	Basic medical services provided at Gacal Budget Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:47.545+03	2025-09-01 20:02:47.545+03	12490	11
26955	Emergency Response Services	Emergency response services at Gacal Budget Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:02:47.563+03	2025-09-01 20:02:47.563+03	12490	27
26956	Counseling & Support Services	Counseling and support services at Gacal Budget Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:47.576+03	2025-09-01 20:02:47.576+03	12490	20
26957	General Medical Services	Basic medical services provided at Samara Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:48.795+03	2025-09-01 20:02:48.795+03	12491	11
26958	Counseling & Support Services	Counseling and support services at Samara Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:48.802+03	2025-09-01 20:02:48.802+03	12491	20
26959	General Medical Services	Basic medical services provided at Al-Dayax Medical Clinic And Laboratory Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:50.303+03	2025-09-01 20:02:50.303+03	12492	11
26960	Counseling & Support Services	Counseling and support services at Al-Dayax Medical Clinic And Laboratory Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:50.31+03	2025-09-01 20:02:50.31+03	12492	20
26961	General Medical Services	Basic medical services provided at Mbassy Medical Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:51.798+03	2025-09-01 20:02:51.798+03	12493	11
26962	Counseling & Support Services	Counseling and support services at Mbassy Medical Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:51.808+03	2025-09-01 20:02:51.808+03	12493	20
26963	General Medical Services	Basic medical services provided at Star Dental Clinics Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:53.095+03	2025-09-01 20:02:53.095+03	12494	11
26964	Counseling & Support Services	Counseling and support services at Star Dental Clinics Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:53.104+03	2025-09-01 20:02:53.104+03	12494	20
26965	General Medical Services	Basic medical services provided at Tawheed Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:54.397+03	2025-09-01 20:02:54.397+03	12495	11
26966	Counseling & Support Services	Counseling and support services at Tawheed Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:54.406+03	2025-09-01 20:02:54.406+03	12495	20
26967	General Medical Services	Basic medical services provided at Dobale Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:55.997+03	2025-09-01 20:02:55.997+03	12496	11
26968	Counseling & Support Services	Counseling and support services at Dobale Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:56.004+03	2025-09-01 20:02:56.004+03	12496	20
26969	General Medical Services	Basic medical services provided at Shifa Maternal And Child Care Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:57.555+03	2025-09-01 20:02:57.555+03	12497	11
26970	Counseling & Support Services	Counseling and support services at Shifa Maternal And Child Care Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:57.566+03	2025-09-01 20:02:57.566+03	12497	20
26971	General Medical Services	Basic medical services provided at Nep Nursing And Rehabilitation Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:59.47+03	2025-09-01 20:02:59.47+03	12498	11
26972	Counseling & Support Services	Counseling and support services at Nep Nursing And Rehabilitation Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:02:59.477+03	2025-09-01 20:02:59.477+03	12498	20
26973	General Medical Services	Basic medical services provided at Sa V Annah Royal Hospital Garissa Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:01.27+03	2025-09-01 20:03:01.27+03	12499	11
26974	Emergency Response Services	Emergency response services at Sa V Annah Royal Hospital Garissa Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:01.277+03	2025-09-01 20:03:01.277+03	12499	27
26975	Counseling & Support Services	Counseling and support services at Sa V Annah Royal Hospital Garissa Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:01.287+03	2025-09-01 20:03:01.287+03	12499	20
26976	General Medical Services	Basic medical services provided at Emirates Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:02.742+03	2025-09-01 20:03:02.742+03	12500	11
26977	Emergency Response Services	Emergency response services at Emirates Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:02.75+03	2025-09-01 20:03:02.75+03	12500	27
26978	Counseling & Support Services	Counseling and support services at Emirates Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:02.758+03	2025-09-01 20:03:02.758+03	12500	20
26979	General Medical Services	Basic medical services provided at Al-Baitul Tiiba Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:04.088+03	2025-09-01 20:03:04.088+03	12501	11
26980	Emergency Response Services	Emergency response services at Al-Baitul Tiiba Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:04.096+03	2025-09-01 20:03:04.096+03	12501	27
26981	Counseling & Support Services	Counseling and support services at Al-Baitul Tiiba Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:04.103+03	2025-09-01 20:03:04.103+03	12501	20
26982	General Medical Services	Basic medical services provided at Jidah Medical Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:05.807+03	2025-09-01 20:03:05.807+03	12502	11
26983	Counseling & Support Services	Counseling and support services at Jidah Medical Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:05.813+03	2025-09-01 20:03:05.813+03	12502	20
26984	General Medical Services	Basic medical services provided at Top Care Orthopaedic And Trauma Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:06.978+03	2025-09-01 20:03:06.978+03	12503	11
26985	Counseling & Support Services	Counseling and support services at Top Care Orthopaedic And Trauma Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:06.984+03	2025-09-01 20:03:06.984+03	12503	20
26986	General Medical Services	Basic medical services provided at An Najah Medical Care Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:08.51+03	2025-09-01 20:03:08.51+03	12504	11
26987	Counseling & Support Services	Counseling and support services at An Najah Medical Care Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:08.517+03	2025-09-01 20:03:08.517+03	12504	20
26988	General Medical Services	Basic medical services provided at Al Qudus Diagnostic Hospital.	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:08.627+03	2025-09-01 20:03:08.627+03	12505	11
26989	Emergency Response Services	Emergency response services at Al Qudus Diagnostic Hospital.	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:08.635+03	2025-09-01 20:03:08.635+03	12505	27
26990	Counseling & Support Services	Counseling and support services at Al Qudus Diagnostic Hospital.	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:08.642+03	2025-09-01 20:03:08.642+03	12505	20
26991	General Medical Services	Basic medical services provided at Salama Wellness Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:10.466+03	2025-09-01 20:03:10.466+03	12506	11
26992	Counseling & Support Services	Counseling and support services at Salama Wellness Centre Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:10.474+03	2025-09-01 20:03:10.474+03	12506	20
26993	General Medical Services	Basic medical services provided at Garissa University Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:11.785+03	2025-09-01 20:03:11.785+03	12507	11
26994	Counseling & Support Services	Counseling and support services at Garissa University Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:11.8+03	2025-09-01 20:03:11.8+03	12507	20
26995	General Medical Services	Basic medical services provided at Madyan Nursing Home Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:13.107+03	2025-09-01 20:03:13.107+03	12508	11
26996	Counseling & Support Services	Counseling and support services at Madyan Nursing Home Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:13.114+03	2025-09-01 20:03:13.114+03	12508	20
26997	General Medical Services	Basic medical services provided at Al-Maqdis Medical Centre Annex Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:14.249+03	2025-09-01 20:03:14.249+03	12509	11
26998	Counseling & Support Services	Counseling and support services at Al-Maqdis Medical Centre Annex Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:14.258+03	2025-09-01 20:03:14.258+03	12509	20
26999	General Medical Services	Basic medical services provided at Bayan Eye Care Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:15.698+03	2025-09-01 20:03:15.698+03	12510	11
27000	Counseling & Support Services	Counseling and support services at Bayan Eye Care Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:15.705+03	2025-09-01 20:03:15.705+03	12510	20
27001	General Medical Services	Basic medical services provided at Al Hadaf Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:16.851+03	2025-09-01 20:03:16.851+03	12511	11
27002	Counseling & Support Services	Counseling and support services at Al Hadaf Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:16.86+03	2025-09-01 20:03:16.86+03	12511	20
27003	General Medical Services	Basic medical services provided at Abuu Amira Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:18.191+03	2025-09-01 20:03:18.191+03	12512	11
27004	Counseling & Support Services	Counseling and support services at Abuu Amira Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:18.198+03	2025-09-01 20:03:18.198+03	12512	20
27005	General Medical Services	Basic medical services provided at International Optica Clinic Garissa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:19.455+03	2025-09-01 20:03:19.455+03	12513	11
27006	Counseling & Support Services	Counseling and support services at International Optica Clinic Garissa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:19.494+03	2025-09-01 20:03:19.494+03	12513	20
27007	General Medical Services	Basic medical services provided at Tolsan Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:21.116+03	2025-09-01 20:03:21.116+03	12514	11
27008	Counseling & Support Services	Counseling and support services at Tolsan Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:21.122+03	2025-09-01 20:03:21.122+03	12514	20
27009	General Medical Services	Basic medical services provided at Malifisa Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:22.47+03	2025-09-01 20:03:22.47+03	12515	11
27010	Emergency Response Services	Emergency response services at Malifisa Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:22.477+03	2025-09-01 20:03:22.477+03	12515	27
27011	Counseling & Support Services	Counseling and support services at Malifisa Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:22.485+03	2025-09-01 20:03:22.485+03	12515	20
27012	General Medical Services	Basic medical services provided at Garissa Eye And Orthodontics Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:23.603+03	2025-09-01 20:03:23.603+03	12516	11
27013	Emergency Response Services	Emergency response services at Garissa Eye And Orthodontics Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:23.61+03	2025-09-01 20:03:23.61+03	12516	27
27014	Counseling & Support Services	Counseling and support services at Garissa Eye And Orthodontics Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:23.624+03	2025-09-01 20:03:23.624+03	12516	20
27015	General Medical Services	Basic medical services provided at Anfal Medical Center Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:25.155+03	2025-09-01 20:03:25.155+03	12517	11
27016	Counseling & Support Services	Counseling and support services at Anfal Medical Center Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:25.162+03	2025-09-01 20:03:25.162+03	12517	20
27017	General Medical Services	Basic medical services provided at Dr Smile Dental Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:26.292+03	2025-09-01 20:03:26.292+03	12518	11
27018	Counseling & Support Services	Counseling and support services at Dr Smile Dental Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:26.298+03	2025-09-01 20:03:26.299+03	12518	20
27019	General Medical Services	Basic medical services provided at Arqam Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:27.741+03	2025-09-01 20:03:27.741+03	12519	11
27020	Counseling & Support Services	Counseling and support services at Arqam Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:27.747+03	2025-09-01 20:03:27.747+03	12519	20
27021	General Medical Services	Basic medical services provided at Waberi Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:28.736+03	2025-09-01 20:03:28.736+03	12520	11
27022	Emergency Response Services	Emergency response services at Waberi Hospital Ltd	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:28.745+03	2025-09-01 20:03:28.745+03	12520	27
27023	Counseling & Support Services	Counseling and support services at Waberi Hospital Ltd	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:28.755+03	2025-09-01 20:03:28.755+03	12520	20
27024	General Medical Services	Basic medical services provided at Reusse Troyer Mission Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:30.118+03	2025-09-01 20:03:30.118+03	12521	11
27025	Counseling & Support Services	Counseling and support services at Reusse Troyer Mission Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:30.125+03	2025-09-01 20:03:30.125+03	12521	20
27026	General Medical Services	Basic medical services provided at F.S.J St. Theresa Asumbi Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:31.722+03	2025-09-01 20:03:31.722+03	12522	11
27027	Emergency Response Services	Emergency response services at F.S.J St. Theresa Asumbi Mission Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:31.729+03	2025-09-01 20:03:31.729+03	12522	27
27028	Counseling & Support Services	Counseling and support services at F.S.J St. Theresa Asumbi Mission Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:31.736+03	2025-09-01 20:03:31.736+03	12522	20
27029	General Medical Services	Basic medical services provided at St Theresa Fsj Asumbi Rodi Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:33.366+03	2025-09-01 20:03:33.366+03	12523	11
27030	Counseling & Support Services	Counseling and support services at St Theresa Fsj Asumbi Rodi Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:33.373+03	2025-09-01 20:03:33.373+03	12523	20
27031	General Medical Services	Basic medical services provided at Afya Research Africa-Mfangano Community Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:34.809+03	2025-09-01 20:03:34.809+03	12524	11
27032	Counseling & Support Services	Counseling and support services at Afya Research Africa-Mfangano Community Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:34.83+03	2025-09-01 20:03:34.83+03	12524	20
27033	General Medical Services	Basic medical services provided at Okitta Nursing And Maternity Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:36.875+03	2025-09-01 20:03:36.875+03	12525	11
27034	Counseling & Support Services	Counseling and support services at Okitta Nursing And Maternity Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:36.886+03	2025-09-01 20:03:36.887+03	12525	20
27035	General Medical Services	Basic medical services provided at Port Florence Community Hospital Homa Bay	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:38.415+03	2025-09-01 20:03:38.415+03	12526	11
27036	Emergency Response Services	Emergency response services at Port Florence Community Hospital Homa Bay	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:38.423+03	2025-09-01 20:03:38.423+03	12526	27
27037	Counseling & Support Services	Counseling and support services at Port Florence Community Hospital Homa Bay	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:38.429+03	2025-09-01 20:03:38.429+03	12526	20
27038	General Medical Services	Basic medical services provided at The Aga Khan Hospital Homabay	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:38.51+03	2025-09-01 20:03:38.51+03	12527	11
27039	Emergency Response Services	Emergency response services at The Aga Khan Hospital Homabay	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:38.516+03	2025-09-01 20:03:38.516+03	12527	27
27040	Counseling & Support Services	Counseling and support services at The Aga Khan Hospital Homabay	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:38.522+03	2025-09-01 20:03:38.522+03	12527	20
27041	General Medical Services	Basic medical services provided at Watta Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:39.865+03	2025-09-01 20:03:39.865+03	12528	11
27042	Counseling & Support Services	Counseling and support services at Watta Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:39.872+03	2025-09-01 20:03:39.872+03	12528	20
27043	General Medical Services	Basic medical services provided at Port Florence Community Hospital Ndhiwa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:41.609+03	2025-09-01 20:03:41.609+03	12529	11
27044	Emergency Response Services	Emergency response services at Port Florence Community Hospital Ndhiwa	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:41.616+03	2025-09-01 20:03:41.616+03	12529	27
27045	Counseling & Support Services	Counseling and support services at Port Florence Community Hospital Ndhiwa	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:41.637+03	2025-09-01 20:03:41.637+03	12529	20
27046	General Medical Services	Basic medical services provided at Katito Medical Centre-Mbita	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:43.447+03	2025-09-01 20:03:43.447+03	12530	11
27047	Counseling & Support Services	Counseling and support services at Katito Medical Centre-Mbita	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:43.461+03	2025-09-01 20:03:43.461+03	12530	20
27048	General Medical Services	Basic medical services provided at Bliss Healthcare Ltd Homabay	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:44.787+03	2025-09-01 20:03:44.787+03	12531	11
27049	Counseling & Support Services	Counseling and support services at Bliss Healthcare Ltd Homabay	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:44.796+03	2025-09-01 20:03:44.796+03	12531	20
27050	General Medical Services	Basic medical services provided at Tudor Healthcare Ltd-Sindo	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:46.35+03	2025-09-01 20:03:46.35+03	12532	11
27051	Counseling & Support Services	Counseling and support services at Tudor Healthcare Ltd-Sindo	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:46.358+03	2025-09-01 20:03:46.358+03	12532	20
27052	General Medical Services	Basic medical services provided at Hawi Family Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:47.891+03	2025-09-01 20:03:47.891+03	12533	11
27053	Emergency Response Services	Emergency response services at Hawi Family Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:03:47.898+03	2025-09-01 20:03:47.898+03	12533	27
27054	Counseling & Support Services	Counseling and support services at Hawi Family Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:47.906+03	2025-09-01 20:03:47.906+03	12533	20
27055	General Medical Services	Basic medical services provided at Manyatta Community Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:49.714+03	2025-09-01 20:03:49.714+03	12534	11
27056	Counseling & Support Services	Counseling and support services at Manyatta Community Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:49.729+03	2025-09-01 20:03:49.729+03	12534	20
27057	General Medical Services	Basic medical services provided at Nguono Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:51.187+03	2025-09-01 20:03:51.187+03	12535	11
27058	Counseling & Support Services	Counseling and support services at Nguono Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:51.198+03	2025-09-01 20:03:51.198+03	12535	20
27059	General Medical Services	Basic medical services provided at Jatriz Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:52.325+03	2025-09-01 20:03:52.325+03	12536	11
27060	Counseling & Support Services	Counseling and support services at Jatriz Medical Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:52.333+03	2025-09-01 20:03:52.333+03	12536	20
27061	General Medical Services	Basic medical services provided at Flo Dental Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:53.496+03	2025-09-01 20:03:53.496+03	12537	11
27062	Counseling & Support Services	Counseling and support services at Flo Dental Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:53.504+03	2025-09-01 20:03:53.504+03	12537	20
27063	General Medical Services	Basic medical services provided at Raksha International Medical Services Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:54.904+03	2025-09-01 20:03:54.904+03	12538	11
27064	Counseling & Support Services	Counseling and support services at Raksha International Medical Services Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:54.935+03	2025-09-01 20:03:54.935+03	12538	20
27065	General Medical Services	Basic medical services provided at Equity Afia Homabay Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:56.698+03	2025-09-01 20:03:56.698+03	12539	11
27066	Counseling & Support Services	Counseling and support services at Equity Afia Homabay Medical Center	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:56.724+03	2025-09-01 20:03:56.724+03	12539	20
27067	General Medical Services	Basic medical services provided at Rehema Hospice And Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:58.406+03	2025-09-01 20:03:58.406+03	12540	11
27068	Counseling & Support Services	Counseling and support services at Rehema Hospice And Clinic Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:03:58.415+03	2025-09-01 20:03:58.415+03	12540	20
27069	General Medical Services	Basic medical services provided at Perisqure Medical Clinics And Laboratories	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:00.484+03	2025-09-01 20:04:00.484+03	12541	11
27070	Counseling & Support Services	Counseling and support services at Perisqure Medical Clinics And Laboratories	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:00.494+03	2025-09-01 20:04:00.494+03	12541	20
27071	General Medical Services	Basic medical services provided at Isiolo Regional Hospital-Barracks	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:02.748+03	2025-09-01 20:04:02.748+03	12542	11
27072	Emergency Response Services	Emergency response services at Isiolo Regional Hospital-Barracks	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:04:02.756+03	2025-09-01 20:04:02.756+03	12542	27
27073	Counseling & Support Services	Counseling and support services at Isiolo Regional Hospital-Barracks	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:02.763+03	2025-09-01 20:04:02.763+03	12542	20
27074	General Medical Services	Basic medical services provided at Aic Isiolo Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:04.886+03	2025-09-01 20:04:04.886+03	12543	11
27075	Counseling & Support Services	Counseling and support services at Aic Isiolo Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:04.902+03	2025-09-01 20:04:04.902+03	12543	20
27076	General Medical Services	Basic medical services provided at A.C.K Isiolo Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:05.153+03	2025-09-01 20:04:05.153+03	12544	11
27077	Counseling & Support Services	Counseling and support services at A.C.K Isiolo Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:05.166+03	2025-09-01 20:04:05.166+03	12544	20
27078	General Medical Services	Basic medical services provided at Archers Post Catholic Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:05.432+03	2025-09-01 20:04:05.432+03	12545	11
27079	Counseling & Support Services	Counseling and support services at Archers Post Catholic Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:05.444+03	2025-09-01 20:04:05.444+03	12545	20
27080	General Medical Services	Basic medical services provided at Isiolo Catholic Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:07.392+03	2025-09-01 20:04:07.392+03	12546	11
27081	Counseling & Support Services	Counseling and support services at Isiolo Catholic Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:07.401+03	2025-09-01 20:04:07.401+03	12546	20
27082	General Medical Services	Basic medical services provided at St.John Paul Ii A Vi Matercare Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:08.836+03	2025-09-01 20:04:08.836+03	12547	11
27083	Emergency Response Services	Emergency response services at St.John Paul Ii A Vi Matercare Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:04:08.852+03	2025-09-01 20:04:08.852+03	12547	27
27084	Counseling & Support Services	Counseling and support services at St.John Paul Ii A Vi Matercare Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:08.866+03	2025-09-01 20:04:08.866+03	12547	20
27085	General Medical Services	Basic medical services provided at Camp Garba Catholic Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:10.584+03	2025-09-01 20:04:10.584+03	12548	11
27086	Counseling & Support Services	Counseling and support services at Camp Garba Catholic Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:10.593+03	2025-09-01 20:04:10.593+03	12548	20
27087	General Medical Services	Basic medical services provided at Catholic Dispensary Ngaremara	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:12.322+03	2025-09-01 20:04:12.322+03	12549	11
27088	Counseling & Support Services	Counseling and support services at Catholic Dispensary Ngaremara	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:12.333+03	2025-09-01 20:04:12.333+03	12549	20
27089	General Medical Services	Basic medical services provided at Leparua Community Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:14.201+03	2025-09-01 20:04:14.201+03	12550	11
27090	Counseling & Support Services	Counseling and support services at Leparua Community Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:14.218+03	2025-09-01 20:04:14.218+03	12550	20
27091	General Medical Services	Basic medical services provided at Pepo La Tumaini Jangwani Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:16.344+03	2025-09-01 20:04:16.344+03	12551	11
27092	Counseling & Support Services	Counseling and support services at Pepo La Tumaini Jangwani Health Centre	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:16.355+03	2025-09-01 20:04:16.355+03	12551	20
27093	General Medical Services	Basic medical services provided at Iqra Medical Centre And Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:18.405+03	2025-09-01 20:04:18.405+03	12552	11
27094	Counseling & Support Services	Counseling and support services at Iqra Medical Centre And Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:18.421+03	2025-09-01 20:04:18.421+03	12552	20
27095	General Medical Services	Basic medical services provided at Isiolo County Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:18.526+03	2025-09-01 20:04:18.526+03	12553	11
27096	Counseling & Support Services	Counseling and support services at Isiolo County Nursing Home	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:18.535+03	2025-09-01 20:04:18.535+03	12553	20
27097	General Medical Services	Basic medical services provided at Kulamawe Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:19.78+03	2025-09-01 20:04:19.78+03	12554	11
27098	Counseling & Support Services	Counseling and support services at Kulamawe Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:19.801+03	2025-09-01 20:04:19.801+03	12554	20
27099	General Medical Services	Basic medical services provided at Down Town Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:21.603+03	2025-09-01 20:04:21.603+03	12555	11
27100	Counseling & Support Services	Counseling and support services at Down Town Medical Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:21.611+03	2025-09-01 20:04:21.611+03	12555	20
27101	General Medical Services	Basic medical services provided at Healthpact Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:23.112+03	2025-09-01 20:04:23.112+03	12556	11
27102	Emergency Response Services	Emergency response services at Healthpact Hospital	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:04:23.121+03	2025-09-01 20:04:23.121+03	12556	27
27103	Counseling & Support Services	Counseling and support services at Healthpact Hospital	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:23.128+03	2025-09-01 20:04:23.128+03	12556	20
27104	General Medical Services	Basic medical services provided at Simba Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:24.372+03	2025-09-01 20:04:24.372+03	12557	11
27105	Counseling & Support Services	Counseling and support services at Simba Clinic	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:24.378+03	2025-09-01 20:04:24.378+03	12557	20
27106	General Medical Services	Basic medical services provided at Waso Aipca Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:24.493+03	2025-09-01 20:04:24.493+03	12558	11
27107	Counseling & Support Services	Counseling and support services at Waso Aipca Dispensary	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:24.501+03	2025-09-01 20:04:24.501+03	12558	20
27108	General Medical Services	Basic medical services provided at Almas Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:26.184+03	2025-09-01 20:04:26.184+03	12559	11
27109	Counseling & Support Services	Counseling and support services at Almas Medical Services	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:26.2+03	2025-09-01 20:04:26.2+03	12559	20
27110	General Medical Services	Basic medical services provided at Elephant Dental Isiolo	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:27.824+03	2025-09-01 20:04:27.824+03	12560	11
27111	Counseling & Support Services	Counseling and support services at Elephant Dental Isiolo	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:27.83+03	2025-09-01 20:04:27.83+03	12560	20
27112	General Medical Services	Basic medical services provided at Galaxy Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:29.321+03	2025-09-01 20:04:29.321+03	12561	11
27113	Emergency Response Services	Emergency response services at Galaxy Hospital Limited	f	Paid	KES	24/7	Monday - Sunday	f	t	2025-09-01 20:04:29.328+03	2025-09-01 20:04:29.328+03	12561	27
27114	Counseling & Support Services	Counseling and support services at Galaxy Hospital Limited	f	Paid	KES	8:00 AM - 5:00 PM	Monday - Friday	t	t	2025-09-01 20:04:29.336+03	2025-09-01 20:04:29.336+03	12561	20
\.


--
-- TOC entry 4084 (class 0 OID 67288)
-- Dependencies: 257
-- Data for Name: gbv_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.gbv_categories (gbv_category_id, category_name, description, icon_url) FROM stdin;
1	Physical Violence	Physical harm or injury inflicted on a person	
2	Sexual Violence	Any sexual act or attempt to obtain a sexual act by violence or coercion	
3	Emotional/Psychological Violence	Verbal abuse, threats, intimidation, or other psychological harm	
4	Economic Violence	Control over financial resources, employment, or economic opportunities	
5	Intimate Partner Violence	Physical, sexual, or psychological harm by current/former partners	
6	Child Marriage	Marriage where parties are under 18	
7	Female Genital Mutilation	Non-medical removal of external female genitalia	
8	Human Trafficking	Recruitment and exploitation of persons	
9	Psychological Violence	Emotional abuse, threats, intimidation	
10	Stalking	Repeated unwanted attention and harassment	
11	Honor-based Violence	Violence to protect/restore family honor	
12	Technology-facilitated Violence	Cyberstalking and online harassment	
13	LGBTQ+ Violence	Violence based on sexual orientation/gender identity	
14	Disability-based Violence	Violence targeting individuals with disabilities	
15	Elder Abuse	Physical, sexual, emotional, or financial abuse of older adults	
16	Workplace Violence	Violence, harassment, or intimidation at work	
17	Educational Violence	Violence, harassment, or discrimination in education	
\.


--
-- TOC entry 4086 (class 0 OID 67298)
-- Dependencies: 259
-- Data for Name: infrastructure_types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.infrastructure_types (infrastructure_type_id, type_name, description) FROM stdin;
1	Building	Physical building structure
2	Medical Equipment	Medical and diagnostic equipment
3	Furniture	Furniture and fixtures
4	IT Equipment	Computers and information technology equipment
5	Communication Equipment	Telephones, radios, and communication devices
6	Transportation	Vehicles and transportation equipment
7	Security Equipment	Security and safety equipment
8	Utilities	Water, electricity, and utility systems
9	Recreational Facilities	Recreation and leisure facilities
10	Storage Facilities	Storage and warehouse facilities
\.


--
-- TOC entry 4074 (class 0 OID 67230)
-- Dependencies: 247
-- Data for Name: mobile_device_sessions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mobile_device_sessions (device_id, notification_enabled, dark_mode_enabled, preferred_language, latitude, longitude, location_updated_at, location_permission_granted, is_active, last_active_at, created_at, updated_at, game_high_score) FROM stdin;
\.


--
-- TOC entry 4076 (class 0 OID 67236)
-- Dependencies: 249
-- Data for Name: mobile_device_usage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mobile_device_usage (usage_id, feature_name, feature_category, usage_count, first_used, last_used, additional_data, created_at, device_id) FROM stdin;
\.


--
-- TOC entry 4127 (class 0 OID 67790)
-- Dependencies: 300
-- Data for Name: music; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.music (music_id, name, description, link, artist, duration, genre, is_active, created_at, updated_at, created_by, updated_by, music_file) FROM stdin;
\.


--
-- TOC entry 4129 (class 0 OID 67798)
-- Dependencies: 302
-- Data for Name: music_plays; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.music_plays (play_id, played_at, ip_address, user_agent, session_duration, music_id, user_id) FROM stdin;
\.


--
-- TOC entry 4088 (class 0 OID 67308)
-- Dependencies: 261
-- Data for Name: operational_statuses; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.operational_statuses (operational_status_id, status_name, description, sort_order) FROM stdin;
1	Operational		0
2	Non-Operational		0
3	Under Maintenance		0
4	Temporarily Closed		0
5	Under Construction	Facility is under construction	3
6	Under Renovation	Facility is under renovation	4
7	Permanently Closed	Facility is permanently closed	6
\.


--
-- TOC entry 4090 (class 0 OID 67316)
-- Dependencies: 263
-- Data for Name: owner_types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.owner_types (owner_type_id, type_name, description) FROM stdin;
1	Public	
2	Private	
3	Faith-Based	
4	NGO	
5	Community-Owned	
6	Government	Government ownership
7	Corporate	Corporate ownership
8	Individual	Individual ownership
9	Faith-Based Organization	Religious or faith-based organization
10	Private Sector	Private commercial organization
11	International Organization	International development organization
12	Public-Private Partnership	Joint public-private ownership
\.


--
-- TOC entry 4053 (class 0 OID 67020)
-- Dependencies: 226
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.permissions (permission_id, permission_name, resource_name, action_name, description) FROM stdin;
\.


--
-- TOC entry 4068 (class 0 OID 67087)
-- Dependencies: 241
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.role_permissions (id, granted_at, granted_by, permission_id, role_id) FROM stdin;
\.


--
-- TOC entry 4092 (class 0 OID 67324)
-- Dependencies: 265
-- Data for Name: service_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.service_categories (service_category_id, category_name, description, icon_url) FROM stdin;
1	Health Services		
2	Security Services		
3	Legal Services		
4	Counseling Services		
5	Emergency Services		
6	Pharmacy Services	Services related to pharmacy services	
7	Specialist Services	Services related to specialist services	
8	Telemedicine Services	Services related to telemedicine services	
9	Hospital Services	Services related to hospital services	
10	Clinic Services	Services related to clinic services	
11	Medical Services	Services related to medical services	
12	Care Services	Services related to care services	
13	Consultation Services	Services related to consultation services	
14	Surgical Services	Services related to surgical services	
15	Treatment Services	Services related to treatment services	
16	Therapy Services	Services related to therapy services	
17	Diagnostic Services	Services related to diagnostic services	
18	Outpatient Services	Services related to outpatient services	
19	Inpatient Services	Services related to inpatient services	
20	Counseling & Support	Psychological and emotional support services	
21	Legal Aid	Legal assistance and representation services	
22	Shelter & Housing	Temporary and emergency housing services	
23	Education & Training	Educational and training programs	
24	Economic Empowerment	Economic and financial support services	
25	Child Protection	Child welfare and protection services	
26	Community Outreach	Community engagement and awareness programs	
27	Emergency Response	Emergency and crisis intervention services	
28	Rehabilitation	Physical and psychological rehabilitation services	
29	Prevention Services	Prevention and awareness programs	
30	Advocacy	Advocacy and policy support services	
\.


--
-- TOC entry 4064 (class 0 OID 67069)
-- Dependencies: 237
-- Data for Name: user_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_profiles (profile_id, avatar_url, bio, department, job_title, notification_preferences, created_at, updated_at, user_id) FROM stdin;
1	/static/assets/img/brand/hodi app logo.png				{}	2025-08-29 00:49:25.692+03	2025-08-29 00:49:25.692+03	1
\.


--
-- TOC entry 4070 (class 0 OID 67093)
-- Dependencies: 243
-- Data for Name: user_role_assignments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_role_assignments (id, assigned_at, expires_at, assigned_by, role_id, user_id) FROM stdin;
\.


--
-- TOC entry 4055 (class 0 OID 67028)
-- Dependencies: 228
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_roles (role_id, role_name, description, is_system_role, created_at) FROM stdin;
\.


--
-- TOC entry 4071 (class 0 OID 67098)
-- Dependencies: 244
-- Data for Name: user_sessions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_sessions (session_id, ip_address, latitude, longitude, session_data, is_active, created_at, last_activity_at, expires_at, ended_at, user_id, game_high_score) FROM stdin;
Vnaye5wPiddPEM7W0qHs1DRgr5GNa-b2bT5LxdqI0_Q	127.0.0.1	\N	\N	{}	t	2025-09-01 09:08:26.903+03	2025-09-01 09:08:26.903+03	2025-09-02 09:08:26.903+03	\N	1	0
duMedKlpd5gJJuwg32amCgzzod5RH_6CBqTUjU4igGw	127.0.0.1	\N	\N	{}	t	2025-08-29 00:49:53.105+03	2025-08-29 00:49:53.105+03	2025-08-30 00:49:53.105+03	\N	1	0
\.


--
-- TOC entry 4057 (class 0 OID 67036)
-- Dependencies: 230
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (password, user_id, full_name, email, phone_number, is_active, verified, password_reset_token, password_changed_at, created_at, updated_at, is_staff, is_superuser, username, last_login, date_joined) FROM stdin;
pbkdf2_sha256$600000$hXd6ETFgEAam2eGCBDBOz8$s73NLaFIsd1pB59bSlR8n5TUvLZhWPiyuXZsQAQkxuI=	1	admin	admin@gvrc.com	0114269500	t	t		2025-08-29 00:49:24.809+03	2025-08-29 00:49:24.809+03	2025-08-29 00:49:24.809+03	t	t	admin@gvrc.com	2025-09-01 09:08:26.932+03	2025-08-29 00:49:24.809+03
	2	ETL System	etl@system.local	+254700000000	t	f		2025-09-01 13:20:58.566+03	2025-09-01 13:20:58.566+03	2025-09-01 13:20:58.566+03	f	f	etl_system	\N	2025-09-01 13:20:58.566+03
\.


--
-- TOC entry 4059 (class 0 OID 67050)
-- Dependencies: 232
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 4061 (class 0 OID 67056)
-- Dependencies: 234
-- Data for Name: users_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 4098 (class 0 OID 67367)
-- Dependencies: 271
-- Data for Name: wards; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.wards (ward_id, ward_name, ward_code, created_at, updated_at, constituency_id) FROM stdin;
191	Kabarnet	EE2155E9	2025-09-01 19:56:33.888+03	2025-09-01 19:56:33.888+03	127
192	Eldama Ravine	F43F5053	2025-09-01 19:56:35.246+03	2025-09-01 19:56:35.246+03	128
193	Eldoret	613EF401	2025-09-01 19:56:37.419+03	2025-09-01 19:56:37.419+03	129
194	Parklands/Highridge	3FD4D1C4	2025-09-01 19:56:37.45+03	2025-09-01 19:56:37.45+03	130
195	Nakuru Ward	E169C76B	2025-09-01 19:56:37.493+03	2025-09-01 19:56:37.493+03	131
196	Bomet Ward	22DC977B	2025-09-01 19:56:37.568+03	2025-09-01 19:56:37.568+03	132
197	Kericho Ward	8BC8C2CB	2025-09-01 19:56:37.607+03	2025-09-01 19:56:37.607+03	133
198	Kisumu Ward	39FEBD9A	2025-09-01 19:56:37.66+03	2025-09-01 19:56:37.66+03	134
199	Bungoma Ward	1EA1D46F	2025-09-01 19:56:37.765+03	2025-09-01 19:56:37.765+03	135
200	Kakamega Ward	E134333A	2025-09-01 19:57:47.735+03	2025-09-01 19:57:47.735+03	136
201	Migori Ward	E981F3E0	2025-09-01 19:58:05.867+03	2025-09-01 19:58:05.867+03	137
202	Busia Ward	6442C350	2025-09-01 19:58:43.605+03	2025-09-01 19:58:43.605+03	138
203	Siaya Ward	5A25BFD2	2025-09-01 19:59:19.613+03	2025-09-01 19:59:19.613+03	139
204	Embu Ward	4ED9D750	2025-09-01 19:59:57.075+03	2025-09-01 19:59:57.075+03	140
205	Meru Ward	C3B97EAD	2025-09-01 20:00:24.368+03	2025-09-01 20:00:24.368+03	141
206	Garissa Ward	93E1DDBA	2025-09-01 20:01:51.301+03	2025-09-01 20:01:51.301+03	142
207	Kisii Ward	7B8B42A6	2025-09-01 20:03:31.688+03	2025-09-01 20:03:31.688+03	143
208	Mombasa Ward	12420C99	2025-09-01 20:03:46.31+03	2025-09-01 20:03:46.31+03	144
209	Isiolo Ward	686808EB	2025-09-01 20:04:02.679+03	2025-09-01 20:04:02.679+03	145
\.


--
-- TOC entry 4136 (class 0 OID 0)
-- Dependencies: 238
-- Name: api_tokens_token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.api_tokens_token_id_seq', 1, false);


--
-- TOC entry 4137 (class 0 OID 0)
-- Dependencies: 286
-- Name: audit_trail_audit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.audit_trail_audit_id_seq', 1, false);


--
-- TOC entry 4138 (class 0 OID 0)
-- Dependencies: 221
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 4139 (class 0 OID 0)
-- Dependencies: 223
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 4140 (class 0 OID 0)
-- Dependencies: 219
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 176, true);


--
-- TOC entry 4141 (class 0 OID 0)
-- Dependencies: 250
-- Name: condition_statuses_condition_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.condition_statuses_condition_status_id_seq', 8, true);


--
-- TOC entry 4142 (class 0 OID 0)
-- Dependencies: 268
-- Name: constituencies_constituency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.constituencies_constituency_id_seq', 145, true);


--
-- TOC entry 4143 (class 0 OID 0)
-- Dependencies: 288
-- Name: contact_interactions_interaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.contact_interactions_interaction_id_seq', 1, false);


--
-- TOC entry 4144 (class 0 OID 0)
-- Dependencies: 252
-- Name: contact_types_contact_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.contact_types_contact_type_id_seq', 15, true);


--
-- TOC entry 4145 (class 0 OID 0)
-- Dependencies: 266
-- Name: counties_county_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.counties_county_id_seq', 104, true);


--
-- TOC entry 4146 (class 0 OID 0)
-- Dependencies: 245
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- TOC entry 4147 (class 0 OID 0)
-- Dependencies: 217
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 44, true);


--
-- TOC entry 4148 (class 0 OID 0)
-- Dependencies: 215
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 46, true);


--
-- TOC entry 4149 (class 0 OID 0)
-- Dependencies: 254
-- Name: document_types_document_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.document_types_document_type_id_seq', 5, true);


--
-- TOC entry 4150 (class 0 OID 0)
-- Dependencies: 297
-- Name: documents_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.documents_document_id_seq', 1, false);


--
-- TOC entry 4151 (class 0 OID 0)
-- Dependencies: 291
-- Name: emergency_chat_conversations_conversation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.emergency_chat_conversations_conversation_id_seq', 1, false);


--
-- TOC entry 4152 (class 0 OID 0)
-- Dependencies: 293
-- Name: emergency_chat_messages_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.emergency_chat_messages_message_id_seq', 1, false);


--
-- TOC entry 4153 (class 0 OID 0)
-- Dependencies: 295
-- Name: emergency_chat_notifications_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.emergency_chat_notifications_notification_id_seq', 1, false);


--
-- TOC entry 4154 (class 0 OID 0)
-- Dependencies: 272
-- Name: facilities_facility_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facilities_facility_id_seq', 12561, true);


--
-- TOC entry 4155 (class 0 OID 0)
-- Dependencies: 274
-- Name: facility_contacts_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facility_contacts_contact_id_seq', 37690, true);


--
-- TOC entry 4156 (class 0 OID 0)
-- Dependencies: 276
-- Name: facility_coordinates_coordinate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facility_coordinates_coordinate_id_seq', 12562, true);


--
-- TOC entry 4157 (class 0 OID 0)
-- Dependencies: 278
-- Name: facility_gbv_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facility_gbv_categories_id_seq', 1, false);


--
-- TOC entry 4158 (class 0 OID 0)
-- Dependencies: 280
-- Name: facility_infrastructure_infrastructure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facility_infrastructure_infrastructure_id_seq', 1, false);


--
-- TOC entry 4159 (class 0 OID 0)
-- Dependencies: 282
-- Name: facility_owners_owner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facility_owners_owner_id_seq', 1, false);


--
-- TOC entry 4160 (class 0 OID 0)
-- Dependencies: 284
-- Name: facility_services_service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facility_services_service_id_seq', 27114, true);


--
-- TOC entry 4161 (class 0 OID 0)
-- Dependencies: 256
-- Name: gbv_categories_gbv_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.gbv_categories_gbv_category_id_seq', 17, true);


--
-- TOC entry 4162 (class 0 OID 0)
-- Dependencies: 258
-- Name: infrastructure_types_infrastructure_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.infrastructure_types_infrastructure_type_id_seq', 10, true);


--
-- TOC entry 4163 (class 0 OID 0)
-- Dependencies: 248
-- Name: mobile_device_usage_usage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mobile_device_usage_usage_id_seq', 1, false);


--
-- TOC entry 4164 (class 0 OID 0)
-- Dependencies: 299
-- Name: music_music_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.music_music_id_seq', 1, false);


--
-- TOC entry 4165 (class 0 OID 0)
-- Dependencies: 301
-- Name: music_plays_play_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.music_plays_play_id_seq', 1, false);


--
-- TOC entry 4166 (class 0 OID 0)
-- Dependencies: 260
-- Name: operational_statuses_operational_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.operational_statuses_operational_status_id_seq', 7, true);


--
-- TOC entry 4167 (class 0 OID 0)
-- Dependencies: 262
-- Name: owner_types_owner_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.owner_types_owner_type_id_seq', 12, true);


--
-- TOC entry 4168 (class 0 OID 0)
-- Dependencies: 225
-- Name: permissions_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.permissions_permission_id_seq', 1, false);


--
-- TOC entry 4169 (class 0 OID 0)
-- Dependencies: 240
-- Name: role_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.role_permissions_id_seq', 1, false);


--
-- TOC entry 4170 (class 0 OID 0)
-- Dependencies: 264
-- Name: service_categories_service_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.service_categories_service_category_id_seq', 30, true);


--
-- TOC entry 4171 (class 0 OID 0)
-- Dependencies: 236
-- Name: user_profiles_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_profiles_profile_id_seq', 1, true);


--
-- TOC entry 4172 (class 0 OID 0)
-- Dependencies: 242
-- Name: user_role_assignments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_role_assignments_id_seq', 1, false);


--
-- TOC entry 4173 (class 0 OID 0)
-- Dependencies: 227
-- Name: user_roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_roles_role_id_seq', 1, false);


--
-- TOC entry 4174 (class 0 OID 0)
-- Dependencies: 231
-- Name: users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_groups_id_seq', 1, false);


--
-- TOC entry 4175 (class 0 OID 0)
-- Dependencies: 229
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);


--
-- TOC entry 4176 (class 0 OID 0)
-- Dependencies: 233
-- Name: users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_permissions_id_seq', 1, false);


--
-- TOC entry 4177 (class 0 OID 0)
-- Dependencies: 270
-- Name: wards_ward_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.wards_ward_id_seq', 209, true);


--
-- TOC entry 3578 (class 2606 OID 67083)
-- Name: api_tokens api_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_tokens
    ADD CONSTRAINT api_tokens_pkey PRIMARY KEY (token_id);


--
-- TOC entry 3581 (class 2606 OID 67085)
-- Name: api_tokens api_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_tokens
    ADD CONSTRAINT api_tokens_token_hash_key UNIQUE (token_hash);


--
-- TOC entry 3765 (class 2606 OID 67604)
-- Name: audit_trail audit_trail_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trail
    ADD CONSTRAINT audit_trail_pkey PRIMARY KEY (audit_id);


--
-- TOC entry 3524 (class 2606 OID 67017)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 3529 (class 2606 OID 67003)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 3532 (class 2606 OID 66992)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3526 (class 2606 OID 66984)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 3519 (class 2606 OID 66994)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 3521 (class 2606 OID 66978)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 3775 (class 2606 OID 67645)
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- TOC entry 3777 (class 2606 OID 67647)
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- TOC entry 3628 (class 2606 OID 67266)
-- Name: condition_statuses condition_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.condition_statuses
    ADD CONSTRAINT condition_statuses_pkey PRIMARY KEY (condition_status_id);


--
-- TOC entry 3631 (class 2606 OID 67268)
-- Name: condition_statuses condition_statuses_status_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.condition_statuses
    ADD CONSTRAINT condition_statuses_status_name_key UNIQUE (status_name);


--
-- TOC entry 3687 (class 2606 OID 67365)
-- Name: constituencies constituencies_constituency_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constituencies
    ADD CONSTRAINT constituencies_constituency_code_key UNIQUE (constituency_code);


--
-- TOC entry 3690 (class 2606 OID 67363)
-- Name: constituencies constituencies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constituencies
    ADD CONSTRAINT constituencies_pkey PRIMARY KEY (constituency_id);


--
-- TOC entry 3772 (class 2606 OID 67610)
-- Name: contact_interactions contact_interactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contact_interactions
    ADD CONSTRAINT contact_interactions_pkey PRIMARY KEY (interaction_id);


--
-- TOC entry 3634 (class 2606 OID 67274)
-- Name: contact_types contact_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contact_types
    ADD CONSTRAINT contact_types_pkey PRIMARY KEY (contact_type_id);


--
-- TOC entry 3637 (class 2606 OID 67276)
-- Name: contact_types contact_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contact_types
    ADD CONSTRAINT contact_types_type_name_key UNIQUE (type_name);


--
-- TOC entry 3679 (class 2606 OID 67357)
-- Name: counties counties_county_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.counties
    ADD CONSTRAINT counties_county_code_key UNIQUE (county_code);


--
-- TOC entry 3681 (class 2606 OID 67355)
-- Name: counties counties_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.counties
    ADD CONSTRAINT counties_pkey PRIMARY KEY (county_id);


--
-- TOC entry 3568 (class 2606 OID 67065)
-- Name: custom_tokens custom_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.custom_tokens
    ADD CONSTRAINT custom_tokens_pkey PRIMARY KEY (key);


--
-- TOC entry 3570 (class 2606 OID 67067)
-- Name: custom_tokens custom_tokens_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.custom_tokens
    ADD CONSTRAINT custom_tokens_user_id_key UNIQUE (user_id);


--
-- TOC entry 3607 (class 2606 OID 67217)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3514 (class 2606 OID 66972)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 3516 (class 2606 OID 66970)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3512 (class 2606 OID 66964)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3833 (class 2606 OID 67846)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 3640 (class 2606 OID 67284)
-- Name: document_types document_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_types
    ADD CONSTRAINT document_types_pkey PRIMARY KEY (document_type_id);


--
-- TOC entry 3643 (class 2606 OID 67286)
-- Name: document_types document_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_types
    ADD CONSTRAINT document_types_type_name_key UNIQUE (type_name);


--
-- TOC entry 3814 (class 2606 OID 67750)
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (document_id);


--
-- TOC entry 3788 (class 2606 OID 67662)
-- Name: emergency_chat_conversations emergency_chat_conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_conversations
    ADD CONSTRAINT emergency_chat_conversations_pkey PRIMARY KEY (conversation_id);


--
-- TOC entry 3797 (class 2606 OID 67670)
-- Name: emergency_chat_messages emergency_chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_messages
    ADD CONSTRAINT emergency_chat_messages_pkey PRIMARY KEY (message_id);


--
-- TOC entry 3806 (class 2606 OID 67678)
-- Name: emergency_chat_notifications emergency_chat_notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_notifications
    ADD CONSTRAINT emergency_chat_notifications_pkey PRIMARY KEY (notification_id);


--
-- TOC entry 3703 (class 2606 OID 67406)
-- Name: facilities facilities_facility_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_facility_code_key UNIQUE (facility_code);


--
-- TOC entry 3708 (class 2606 OID 67404)
-- Name: facilities facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_pkey PRIMARY KEY (facility_id);


--
-- TOC entry 3711 (class 2606 OID 67408)
-- Name: facilities facilities_registration_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_registration_number_key UNIQUE (registration_number);


--
-- TOC entry 3722 (class 2606 OID 67414)
-- Name: facility_contacts facility_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_contacts
    ADD CONSTRAINT facility_contacts_pkey PRIMARY KEY (contact_id);


--
-- TOC entry 3728 (class 2606 OID 67420)
-- Name: facility_coordinates facility_coordinates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_coordinates
    ADD CONSTRAINT facility_coordinates_pkey PRIMARY KEY (coordinate_id);


--
-- TOC entry 3734 (class 2606 OID 67460)
-- Name: facility_gbv_categories facility_gbv_categories_facility_id_gbv_category_568d54e0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_gbv_categories
    ADD CONSTRAINT facility_gbv_categories_facility_id_gbv_category_568d54e0_uniq UNIQUE (facility_id, gbv_category_id);


--
-- TOC entry 3737 (class 2606 OID 67426)
-- Name: facility_gbv_categories facility_gbv_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_gbv_categories
    ADD CONSTRAINT facility_gbv_categories_pkey PRIMARY KEY (id);


--
-- TOC entry 3747 (class 2606 OID 67434)
-- Name: facility_infrastructure facility_infrastructure_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_infrastructure
    ADD CONSTRAINT facility_infrastructure_pkey PRIMARY KEY (infrastructure_id);


--
-- TOC entry 3755 (class 2606 OID 67440)
-- Name: facility_owners facility_owners_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_owners
    ADD CONSTRAINT facility_owners_pkey PRIMARY KEY (owner_id);


--
-- TOC entry 3762 (class 2606 OID 67448)
-- Name: facility_services facility_services_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_services
    ADD CONSTRAINT facility_services_pkey PRIMARY KEY (service_id);


--
-- TOC entry 3647 (class 2606 OID 67296)
-- Name: gbv_categories gbv_categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gbv_categories
    ADD CONSTRAINT gbv_categories_category_name_key UNIQUE (category_name);


--
-- TOC entry 3649 (class 2606 OID 67294)
-- Name: gbv_categories gbv_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gbv_categories
    ADD CONSTRAINT gbv_categories_pkey PRIMARY KEY (gbv_category_id);


--
-- TOC entry 3652 (class 2606 OID 67304)
-- Name: infrastructure_types infrastructure_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.infrastructure_types
    ADD CONSTRAINT infrastructure_types_pkey PRIMARY KEY (infrastructure_type_id);


--
-- TOC entry 3655 (class 2606 OID 67306)
-- Name: infrastructure_types infrastructure_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.infrastructure_types
    ADD CONSTRAINT infrastructure_types_type_name_key UNIQUE (type_name);


--
-- TOC entry 3615 (class 2606 OID 67234)
-- Name: mobile_device_sessions mobile_device_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mobile_device_sessions
    ADD CONSTRAINT mobile_device_sessions_pkey PRIMARY KEY (device_id);


--
-- TOC entry 3623 (class 2606 OID 67253)
-- Name: mobile_device_usage mobile_device_usage_device_id_feature_name_2689baf9_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mobile_device_usage
    ADD CONSTRAINT mobile_device_usage_device_id_feature_name_2689baf9_uniq UNIQUE (device_id, feature_name);


--
-- TOC entry 3625 (class 2606 OID 67242)
-- Name: mobile_device_usage mobile_device_usage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mobile_device_usage
    ADD CONSTRAINT mobile_device_usage_pkey PRIMARY KEY (usage_id);


--
-- TOC entry 3822 (class 2606 OID 67796)
-- Name: music music_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.music
    ADD CONSTRAINT music_pkey PRIMARY KEY (music_id);


--
-- TOC entry 3827 (class 2606 OID 67804)
-- Name: music_plays music_plays_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.music_plays
    ADD CONSTRAINT music_plays_pkey PRIMARY KEY (play_id);


--
-- TOC entry 3659 (class 2606 OID 67312)
-- Name: operational_statuses operational_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.operational_statuses
    ADD CONSTRAINT operational_statuses_pkey PRIMARY KEY (operational_status_id);


--
-- TOC entry 3662 (class 2606 OID 67314)
-- Name: operational_statuses operational_statuses_status_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.operational_statuses
    ADD CONSTRAINT operational_statuses_status_name_key UNIQUE (status_name);


--
-- TOC entry 3664 (class 2606 OID 67320)
-- Name: owner_types owner_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.owner_types
    ADD CONSTRAINT owner_types_pkey PRIMARY KEY (owner_type_id);


--
-- TOC entry 3668 (class 2606 OID 67322)
-- Name: owner_types owner_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.owner_types
    ADD CONSTRAINT owner_types_type_name_key UNIQUE (type_name);


--
-- TOC entry 3535 (class 2606 OID 67026)
-- Name: permissions permissions_permission_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_permission_name_key UNIQUE (permission_name);


--
-- TOC entry 3537 (class 2606 OID 67024)
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (permission_id);


--
-- TOC entry 3587 (class 2606 OID 67091)
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3590 (class 2606 OID 67160)
-- Name: role_permissions role_permissions_role_id_permission_id_04f77df0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_permission_id_04f77df0_uniq UNIQUE (role_id, permission_id);


--
-- TOC entry 3672 (class 2606 OID 67332)
-- Name: service_categories service_categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.service_categories
    ADD CONSTRAINT service_categories_category_name_key UNIQUE (category_name);


--
-- TOC entry 3674 (class 2606 OID 67330)
-- Name: service_categories service_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.service_categories
    ADD CONSTRAINT service_categories_pkey PRIMARY KEY (service_category_id);


--
-- TOC entry 3572 (class 2606 OID 67075)
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (profile_id);


--
-- TOC entry 3574 (class 2606 OID 67077)
-- Name: user_profiles user_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_key UNIQUE (user_id);


--
-- TOC entry 3593 (class 2606 OID 67097)
-- Name: user_role_assignments user_role_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_role_assignments
    ADD CONSTRAINT user_role_assignments_pkey PRIMARY KEY (id);


--
-- TOC entry 3597 (class 2606 OID 67180)
-- Name: user_role_assignments user_role_assignments_user_id_role_id_db8b4891_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_role_assignments
    ADD CONSTRAINT user_role_assignments_user_id_role_id_db8b4891_uniq UNIQUE (user_id, role_id);


--
-- TOC entry 3539 (class 2606 OID 67032)
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (role_id);


--
-- TOC entry 3542 (class 2606 OID 67034)
-- Name: user_roles user_roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_name_key UNIQUE (role_name);


--
-- TOC entry 3602 (class 2606 OID 67104)
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (session_id);


--
-- TOC entry 3545 (class 2606 OID 67044)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3556 (class 2606 OID 67054)
-- Name: users_groups users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3559 (class 2606 OID 67111)
-- Name: users_groups users_groups_user_id_group_id_fc7788e8_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_group_id_fc7788e8_uniq UNIQUE (user_id, group_id);


--
-- TOC entry 3548 (class 2606 OID 67046)
-- Name: users users_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_number_key UNIQUE (phone_number);


--
-- TOC entry 3550 (class 2606 OID 67042)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 3562 (class 2606 OID 67060)
-- Name: users_user_permissions users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3565 (class 2606 OID 67125)
-- Name: users_user_permissions users_user_permissions_user_id_permission_id_3b86cbdf_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_permission_id_3b86cbdf_uniq UNIQUE (user_id, permission_id);


--
-- TOC entry 3553 (class 2606 OID 67048)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 3694 (class 2606 OID 67371)
-- Name: wards wards_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wards
    ADD CONSTRAINT wards_pkey PRIMARY KEY (ward_id);


--
-- TOC entry 3698 (class 2606 OID 67373)
-- Name: wards wards_ward_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wards
    ADD CONSTRAINT wards_ward_code_key UNIQUE (ward_code);


--
-- TOC entry 3575 (class 1259 OID 67158)
-- Name: api_tokens_expires_a047d2_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX api_tokens_expires_a047d2_idx ON public.api_tokens USING btree (expires_at);


--
-- TOC entry 3576 (class 1259 OID 67157)
-- Name: api_tokens_is_acti_949075_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX api_tokens_is_acti_949075_idx ON public.api_tokens USING btree (is_active);


--
-- TOC entry 3579 (class 1259 OID 67154)
-- Name: api_tokens_token_hash_70d52dcc_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX api_tokens_token_hash_70d52dcc_like ON public.api_tokens USING btree (token_hash varchar_pattern_ops);


--
-- TOC entry 3582 (class 1259 OID 67155)
-- Name: api_tokens_user_id_2db24e1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX api_tokens_user_id_2db24e1c ON public.api_tokens USING btree (user_id);


--
-- TOC entry 3583 (class 1259 OID 67156)
-- Name: api_tokens_user_id_caf836_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX api_tokens_user_id_caf836_idx ON public.api_tokens USING btree (user_id);


--
-- TOC entry 3766 (class 1259 OID 67616)
-- Name: audit_trail_session_id_43235492; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_trail_session_id_43235492 ON public.audit_trail USING btree (session_id);


--
-- TOC entry 3767 (class 1259 OID 67617)
-- Name: audit_trail_session_id_43235492_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX audit_trail_session_id_43235492_like ON public.audit_trail USING btree (session_id varchar_pattern_ops);


--
-- TOC entry 3522 (class 1259 OID 67018)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 3527 (class 1259 OID 67014)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 3530 (class 1259 OID 67015)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 3517 (class 1259 OID 67000)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 3773 (class 1259 OID 67653)
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- TOC entry 3626 (class 1259 OID 67334)
-- Name: condition_s_status__6509be_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX condition_s_status__6509be_idx ON public.condition_statuses USING btree (status_name);


--
-- TOC entry 3629 (class 1259 OID 67333)
-- Name: condition_statuses_status_name_1f4362dd_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX condition_statuses_status_name_1f4362dd_like ON public.condition_statuses USING btree (status_name varchar_pattern_ops);


--
-- TOC entry 3682 (class 1259 OID 67375)
-- Name: constituenc_constit_b8037d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX constituenc_constit_b8037d_idx ON public.constituencies USING btree (constituency_name);


--
-- TOC entry 3683 (class 1259 OID 67376)
-- Name: constituenc_constit_e8225b_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX constituenc_constit_e8225b_idx ON public.constituencies USING btree (constituency_code);


--
-- TOC entry 3684 (class 1259 OID 67374)
-- Name: constituenc_county__9dc793_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX constituenc_county__9dc793_idx ON public.constituencies USING btree (county_id);


--
-- TOC entry 3685 (class 1259 OID 67388)
-- Name: constituencies_constituency_code_9423bb36_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX constituencies_constituency_code_9423bb36_like ON public.constituencies USING btree (constituency_code varchar_pattern_ops);


--
-- TOC entry 3688 (class 1259 OID 67389)
-- Name: constituencies_county_id_308f52ae; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX constituencies_county_id_308f52ae ON public.constituencies USING btree (county_id);


--
-- TOC entry 3768 (class 1259 OID 67628)
-- Name: contact_interactions_contact_id_f5f4544a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_interactions_contact_id_f5f4544a ON public.contact_interactions USING btree (contact_id);


--
-- TOC entry 3769 (class 1259 OID 67629)
-- Name: contact_interactions_device_id_aedd942e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_interactions_device_id_aedd942e ON public.contact_interactions USING btree (device_id);


--
-- TOC entry 3770 (class 1259 OID 67630)
-- Name: contact_interactions_device_id_aedd942e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_interactions_device_id_aedd942e_like ON public.contact_interactions USING btree (device_id varchar_pattern_ops);


--
-- TOC entry 3632 (class 1259 OID 67336)
-- Name: contact_typ_type_na_65c398_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_typ_type_na_65c398_idx ON public.contact_types USING btree (type_name);


--
-- TOC entry 3635 (class 1259 OID 67335)
-- Name: contact_types_type_name_d45844b9_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contact_types_type_name_d45844b9_like ON public.contact_types USING btree (type_name varchar_pattern_ops);


--
-- TOC entry 3675 (class 1259 OID 67381)
-- Name: counties_county__94451a_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX counties_county__94451a_idx ON public.counties USING btree (county_name);


--
-- TOC entry 3676 (class 1259 OID 67382)
-- Name: counties_county__a59c4f_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX counties_county__a59c4f_idx ON public.counties USING btree (county_code);


--
-- TOC entry 3677 (class 1259 OID 67380)
-- Name: counties_county_code_fde4d419_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX counties_county_code_fde4d419_like ON public.counties USING btree (county_code varchar_pattern_ops);


--
-- TOC entry 3566 (class 1259 OID 67143)
-- Name: custom_tokens_key_e2c9d401_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX custom_tokens_key_e2c9d401_like ON public.custom_tokens USING btree (key varchar_pattern_ops);


--
-- TOC entry 3605 (class 1259 OID 67228)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 3608 (class 1259 OID 67229)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 3831 (class 1259 OID 67848)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 3834 (class 1259 OID 67847)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 3638 (class 1259 OID 67338)
-- Name: document_ty_type_na_0d5fea_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX document_ty_type_na_0d5fea_idx ON public.document_types USING btree (type_name);


--
-- TOC entry 3641 (class 1259 OID 67337)
-- Name: document_types_type_name_09b23418_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX document_types_type_name_09b23418_like ON public.document_types USING btree (type_name varchar_pattern_ops);


--
-- TOC entry 3808 (class 1259 OID 67769)
-- Name: documents_documen_0426e4_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_documen_0426e4_idx ON public.documents USING btree (document_type_id);


--
-- TOC entry 3809 (class 1259 OID 67766)
-- Name: documents_document_type_id_44d85642; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_document_type_id_44d85642 ON public.documents USING btree (document_type_id);


--
-- TOC entry 3810 (class 1259 OID 67767)
-- Name: documents_gbv_category_c51e0c9d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_gbv_category_c51e0c9d ON public.documents USING btree (gbv_category);


--
-- TOC entry 3811 (class 1259 OID 67772)
-- Name: documents_is_acti_a803bb_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_is_acti_a803bb_idx ON public.documents USING btree (is_active);


--
-- TOC entry 3812 (class 1259 OID 67771)
-- Name: documents_is_publ_af3237_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_is_publ_af3237_idx ON public.documents USING btree (is_public);


--
-- TOC entry 3815 (class 1259 OID 67770)
-- Name: documents_uploade_f550b6_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_uploade_f550b6_idx ON public.documents USING btree (uploaded_by);


--
-- TOC entry 3816 (class 1259 OID 67768)
-- Name: documents_uploaded_by_fa4ffa51; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX documents_uploaded_by_fa4ffa51 ON public.documents USING btree (uploaded_by);


--
-- TOC entry 3778 (class 1259 OID 67681)
-- Name: emergency_c_assigne_def626_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_assigne_def626_idx ON public.emergency_chat_conversations USING btree (assigned_admin_id);


--
-- TOC entry 3789 (class 1259 OID 67684)
-- Name: emergency_c_convers_facbbe_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_convers_facbbe_idx ON public.emergency_chat_messages USING btree (conversation_id);


--
-- TOC entry 3779 (class 1259 OID 67682)
-- Name: emergency_c_created_6bac2d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_created_6bac2d_idx ON public.emergency_chat_conversations USING btree (created_at);


--
-- TOC entry 3799 (class 1259 OID 67693)
-- Name: emergency_c_created_cfae1d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_created_cfae1d_idx ON public.emergency_chat_notifications USING btree (created_at);


--
-- TOC entry 3800 (class 1259 OID 67692)
-- Name: emergency_c_is_read_7681b4_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_is_read_7681b4_idx ON public.emergency_chat_notifications USING btree (is_read);


--
-- TOC entry 3790 (class 1259 OID 67689)
-- Name: emergency_c_is_urge_d9f777_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_is_urge_d9f777_idx ON public.emergency_chat_messages USING btree (is_urgent);


--
-- TOC entry 3780 (class 1259 OID 67683)
-- Name: emergency_c_last_me_8a2ac0_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_last_me_8a2ac0_idx ON public.emergency_chat_conversations USING btree (last_message_at);


--
-- TOC entry 3801 (class 1259 OID 67691)
-- Name: emergency_c_notific_98f949_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_notific_98f949_idx ON public.emergency_chat_notifications USING btree (notification_type);


--
-- TOC entry 3781 (class 1259 OID 67680)
-- Name: emergency_c_priorit_4bd477_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_priorit_4bd477_idx ON public.emergency_chat_conversations USING btree (priority);


--
-- TOC entry 3791 (class 1259 OID 67686)
-- Name: emergency_c_sender__3b2a87_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_sender__3b2a87_idx ON public.emergency_chat_messages USING btree (sender_type);


--
-- TOC entry 3792 (class 1259 OID 67685)
-- Name: emergency_c_sender__568497_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_sender__568497_idx ON public.emergency_chat_messages USING btree (sender_id);


--
-- TOC entry 3793 (class 1259 OID 67687)
-- Name: emergency_c_sent_at_3a3fbe_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_sent_at_3a3fbe_idx ON public.emergency_chat_messages USING btree (sent_at);


--
-- TOC entry 3782 (class 1259 OID 67679)
-- Name: emergency_c_status_51cf71_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_status_51cf71_idx ON public.emergency_chat_conversations USING btree (status);


--
-- TOC entry 3794 (class 1259 OID 67688)
-- Name: emergency_c_status_dc2d02_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_status_dc2d02_idx ON public.emergency_chat_messages USING btree (status);


--
-- TOC entry 3802 (class 1259 OID 67690)
-- Name: emergency_c_user_id_611b40_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_c_user_id_611b40_idx ON public.emergency_chat_notifications USING btree (user_id);


--
-- TOC entry 3783 (class 1259 OID 67709)
-- Name: emergency_chat_conversations_assigned_admin_id_c2c47763; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_conversations_assigned_admin_id_c2c47763 ON public.emergency_chat_conversations USING btree (assigned_admin_id);


--
-- TOC entry 3784 (class 1259 OID 67710)
-- Name: emergency_chat_conversations_last_message_by_id_72260c9b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_conversations_last_message_by_id_72260c9b ON public.emergency_chat_conversations USING btree (last_message_by_id);


--
-- TOC entry 3785 (class 1259 OID 67711)
-- Name: emergency_chat_conversations_mobile_session_id_58959a4d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_conversations_mobile_session_id_58959a4d ON public.emergency_chat_conversations USING btree (mobile_session_id);


--
-- TOC entry 3786 (class 1259 OID 67712)
-- Name: emergency_chat_conversations_mobile_session_id_58959a4d_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_conversations_mobile_session_id_58959a4d_like ON public.emergency_chat_conversations USING btree (mobile_session_id varchar_pattern_ops);


--
-- TOC entry 3795 (class 1259 OID 67723)
-- Name: emergency_chat_messages_conversation_id_4702a48a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_messages_conversation_id_4702a48a ON public.emergency_chat_messages USING btree (conversation_id);


--
-- TOC entry 3798 (class 1259 OID 67724)
-- Name: emergency_chat_messages_sender_id_3f59dcfd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_messages_sender_id_3f59dcfd ON public.emergency_chat_messages USING btree (sender_id);


--
-- TOC entry 3803 (class 1259 OID 67741)
-- Name: emergency_chat_notifications_conversation_id_ddf27239; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_notifications_conversation_id_ddf27239 ON public.emergency_chat_notifications USING btree (conversation_id);


--
-- TOC entry 3804 (class 1259 OID 67742)
-- Name: emergency_chat_notifications_message_id_d4d8bfe6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_notifications_message_id_d4d8bfe6 ON public.emergency_chat_notifications USING btree (message_id);


--
-- TOC entry 3807 (class 1259 OID 67740)
-- Name: emergency_chat_notifications_user_id_c5187218; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX emergency_chat_notifications_user_id_c5187218 ON public.emergency_chat_notifications USING btree (user_id);


--
-- TOC entry 3700 (class 1259 OID 67491)
-- Name: facilities_created_by_522b765d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_created_by_522b765d ON public.facilities USING btree (created_by);


--
-- TOC entry 3701 (class 1259 OID 67489)
-- Name: facilities_facility_code_a17644aa_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_facility_code_a17644aa_like ON public.facilities USING btree (facility_code varchar_pattern_ops);


--
-- TOC entry 3704 (class 1259 OID 67451)
-- Name: facilities_is_acti_76f1be_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_is_acti_76f1be_idx ON public.facilities USING btree (is_active);


--
-- TOC entry 3705 (class 1259 OID 67450)
-- Name: facilities_operati_28f767_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_operati_28f767_idx ON public.facilities USING btree (operational_status_id);


--
-- TOC entry 3706 (class 1259 OID 67492)
-- Name: facilities_operational_status_id_946bd007; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_operational_status_id_946bd007 ON public.facilities USING btree (operational_status_id);


--
-- TOC entry 3709 (class 1259 OID 67490)
-- Name: facilities_registration_number_22655837_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_registration_number_22655837_like ON public.facilities USING btree (registration_number varchar_pattern_ops);


--
-- TOC entry 3712 (class 1259 OID 67493)
-- Name: facilities_updated_by_c7d06497; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_updated_by_c7d06497 ON public.facilities USING btree (updated_by);


--
-- TOC entry 3713 (class 1259 OID 67449)
-- Name: facilities_ward_id_93b6d2_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_ward_id_93b6d2_idx ON public.facilities USING btree (ward_id);


--
-- TOC entry 3714 (class 1259 OID 67494)
-- Name: facilities_ward_id_b19cbd31; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facilities_ward_id_b19cbd31 ON public.facilities USING btree (ward_id);


--
-- TOC entry 3724 (class 1259 OID 67456)
-- Name: facility_co_collect_67ee0c_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_co_collect_67ee0c_idx ON public.facility_coordinates USING btree (collection_date);


--
-- TOC entry 3715 (class 1259 OID 67453)
-- Name: facility_co_contact_805b0e_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_co_contact_805b0e_idx ON public.facility_contacts USING btree (contact_type_id);


--
-- TOC entry 3725 (class 1259 OID 67455)
-- Name: facility_co_facilit_12040b_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_co_facilit_12040b_idx ON public.facility_coordinates USING btree (facility_id);


--
-- TOC entry 3716 (class 1259 OID 67452)
-- Name: facility_co_facilit_72d18d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_co_facilit_72d18d_idx ON public.facility_contacts USING btree (facility_id);


--
-- TOC entry 3717 (class 1259 OID 67454)
-- Name: facility_co_is_prim_a3bcec_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_co_is_prim_a3bcec_idx ON public.facility_contacts USING btree (is_primary);


--
-- TOC entry 3718 (class 1259 OID 67515)
-- Name: facility_contacts_contact_type_id_5380d0c8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_contacts_contact_type_id_5380d0c8 ON public.facility_contacts USING btree (contact_type_id);


--
-- TOC entry 3719 (class 1259 OID 67516)
-- Name: facility_contacts_created_by_a5f8561c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_contacts_created_by_a5f8561c ON public.facility_contacts USING btree (created_by);


--
-- TOC entry 3720 (class 1259 OID 67517)
-- Name: facility_contacts_facility_id_c91b40ee; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_contacts_facility_id_c91b40ee ON public.facility_contacts USING btree (facility_id);


--
-- TOC entry 3723 (class 1259 OID 67518)
-- Name: facility_contacts_updated_by_f3e4a7e0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_contacts_updated_by_f3e4a7e0 ON public.facility_contacts USING btree (updated_by);


--
-- TOC entry 3726 (class 1259 OID 67524)
-- Name: facility_coordinates_facility_id_d2e67c35; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_coordinates_facility_id_d2e67c35 ON public.facility_coordinates USING btree (facility_id);


--
-- TOC entry 3729 (class 1259 OID 67457)
-- Name: facility_gb_facilit_2a099c_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_gb_facilit_2a099c_idx ON public.facility_gbv_categories USING btree (facility_id);


--
-- TOC entry 3730 (class 1259 OID 67458)
-- Name: facility_gb_gbv_cat_c7e042_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_gb_gbv_cat_c7e042_idx ON public.facility_gbv_categories USING btree (gbv_category_id);


--
-- TOC entry 3731 (class 1259 OID 67540)
-- Name: facility_gbv_categories_created_by_b61c6e4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_gbv_categories_created_by_b61c6e4f ON public.facility_gbv_categories USING btree (created_by);


--
-- TOC entry 3732 (class 1259 OID 67541)
-- Name: facility_gbv_categories_facility_id_0cf99a99; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_gbv_categories_facility_id_0cf99a99 ON public.facility_gbv_categories USING btree (facility_id);


--
-- TOC entry 3735 (class 1259 OID 67542)
-- Name: facility_gbv_categories_gbv_category_id_3b6325a7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_gbv_categories_gbv_category_id_3b6325a7 ON public.facility_gbv_categories USING btree (gbv_category_id);


--
-- TOC entry 3738 (class 1259 OID 67463)
-- Name: facility_in_conditi_1ec089_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_in_conditi_1ec089_idx ON public.facility_infrastructure USING btree (condition_status_id);


--
-- TOC entry 3739 (class 1259 OID 67461)
-- Name: facility_in_facilit_3980d5_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_in_facilit_3980d5_idx ON public.facility_infrastructure USING btree (facility_id);


--
-- TOC entry 3740 (class 1259 OID 67462)
-- Name: facility_in_infrast_970d40_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_in_infrast_970d40_idx ON public.facility_infrastructure USING btree (infrastructure_type_id);


--
-- TOC entry 3741 (class 1259 OID 67786)
-- Name: facility_in_is_acti_354d9a_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_in_is_acti_354d9a_idx ON public.facility_infrastructure USING btree (is_active);


--
-- TOC entry 3742 (class 1259 OID 67558)
-- Name: facility_infrastructure_condition_status_id_382dd3f9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_infrastructure_condition_status_id_382dd3f9 ON public.facility_infrastructure USING btree (condition_status_id);


--
-- TOC entry 3743 (class 1259 OID 67787)
-- Name: facility_infrastructure_created_by_003846c8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_infrastructure_created_by_003846c8 ON public.facility_infrastructure USING btree (created_by);


--
-- TOC entry 3744 (class 1259 OID 67559)
-- Name: facility_infrastructure_facility_id_42b8797f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_infrastructure_facility_id_42b8797f ON public.facility_infrastructure USING btree (facility_id);


--
-- TOC entry 3745 (class 1259 OID 67560)
-- Name: facility_infrastructure_infrastructure_type_id_c1c3a8d3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_infrastructure_infrastructure_type_id_c1c3a8d3 ON public.facility_infrastructure USING btree (infrastructure_type_id);


--
-- TOC entry 3748 (class 1259 OID 67788)
-- Name: facility_infrastructure_updated_by_91040b96; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_infrastructure_updated_by_91040b96 ON public.facility_infrastructure USING btree (updated_by);


--
-- TOC entry 3749 (class 1259 OID 67464)
-- Name: facility_ow_facilit_21de47_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_ow_facilit_21de47_idx ON public.facility_owners USING btree (facility_id);


--
-- TOC entry 3750 (class 1259 OID 67465)
-- Name: facility_ow_owner_t_a26f8d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_ow_owner_t_a26f8d_idx ON public.facility_owners USING btree (owner_type_id);


--
-- TOC entry 3751 (class 1259 OID 67581)
-- Name: facility_owners_created_by_6c9f6f73; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_owners_created_by_6c9f6f73 ON public.facility_owners USING btree (created_by);


--
-- TOC entry 3752 (class 1259 OID 67582)
-- Name: facility_owners_facility_id_36e99bf4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_owners_facility_id_36e99bf4 ON public.facility_owners USING btree (facility_id);


--
-- TOC entry 3753 (class 1259 OID 67583)
-- Name: facility_owners_owner_type_id_7dea0d2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_owners_owner_type_id_7dea0d2c ON public.facility_owners USING btree (owner_type_id);


--
-- TOC entry 3756 (class 1259 OID 67584)
-- Name: facility_owners_updated_by_dc292e4e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_owners_updated_by_dc292e4e ON public.facility_owners USING btree (updated_by);


--
-- TOC entry 3757 (class 1259 OID 67466)
-- Name: facility_se_facilit_c92597_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_se_facilit_c92597_idx ON public.facility_services USING btree (facility_id);


--
-- TOC entry 3758 (class 1259 OID 67468)
-- Name: facility_se_is_acti_a1e033_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_se_is_acti_a1e033_idx ON public.facility_services USING btree (is_active);


--
-- TOC entry 3759 (class 1259 OID 67467)
-- Name: facility_se_service_a2b980_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_se_service_a2b980_idx ON public.facility_services USING btree (service_category_id);


--
-- TOC entry 3760 (class 1259 OID 67595)
-- Name: facility_services_facility_id_9e5f55dc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_services_facility_id_9e5f55dc ON public.facility_services USING btree (facility_id);


--
-- TOC entry 3763 (class 1259 OID 67596)
-- Name: facility_services_service_category_id_0c249fbd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX facility_services_service_category_id_0c249fbd ON public.facility_services USING btree (service_category_id);


--
-- TOC entry 3644 (class 1259 OID 67340)
-- Name: gbv_categor_categor_3ededf_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX gbv_categor_categor_3ededf_idx ON public.gbv_categories USING btree (category_name);


--
-- TOC entry 3645 (class 1259 OID 67339)
-- Name: gbv_categories_category_name_9002d128_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX gbv_categories_category_name_9002d128_like ON public.gbv_categories USING btree (category_name varchar_pattern_ops);


--
-- TOC entry 3650 (class 1259 OID 67342)
-- Name: infrastruct_type_na_52876f_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX infrastruct_type_na_52876f_idx ON public.infrastructure_types USING btree (type_name);


--
-- TOC entry 3653 (class 1259 OID 67341)
-- Name: infrastructure_types_type_name_46d1539d_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX infrastructure_types_type_name_46d1539d_like ON public.infrastructure_types USING btree (type_name varchar_pattern_ops);


--
-- TOC entry 3616 (class 1259 OID 67247)
-- Name: mobile_devi_device__b7f94d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_device__b7f94d_idx ON public.mobile_device_usage USING btree (device_id);


--
-- TOC entry 3617 (class 1259 OID 67249)
-- Name: mobile_devi_feature_78b551_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_feature_78b551_idx ON public.mobile_device_usage USING btree (feature_category);


--
-- TOC entry 3618 (class 1259 OID 67248)
-- Name: mobile_devi_feature_d5c975_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_feature_d5c975_idx ON public.mobile_device_usage USING btree (feature_name);


--
-- TOC entry 3619 (class 1259 OID 67250)
-- Name: mobile_devi_first_u_3c06ea_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_first_u_3c06ea_idx ON public.mobile_device_usage USING btree (first_used);


--
-- TOC entry 3609 (class 1259 OID 67243)
-- Name: mobile_devi_is_acti_20527c_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_is_acti_20527c_idx ON public.mobile_device_sessions USING btree (is_active);


--
-- TOC entry 3610 (class 1259 OID 67244)
-- Name: mobile_devi_last_ac_6b5072_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_last_ac_6b5072_idx ON public.mobile_device_sessions USING btree (last_active_at);


--
-- TOC entry 3611 (class 1259 OID 67245)
-- Name: mobile_devi_locatio_228e3a_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_locatio_228e3a_idx ON public.mobile_device_sessions USING btree (location_permission_granted);


--
-- TOC entry 3612 (class 1259 OID 67246)
-- Name: mobile_devi_preferr_c75d7d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_devi_preferr_c75d7d_idx ON public.mobile_device_sessions USING btree (preferred_language);


--
-- TOC entry 3613 (class 1259 OID 67251)
-- Name: mobile_device_sessions_device_id_706334c7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_device_sessions_device_id_706334c7_like ON public.mobile_device_sessions USING btree (device_id varchar_pattern_ops);


--
-- TOC entry 3620 (class 1259 OID 67259)
-- Name: mobile_device_usage_device_id_abcd2738; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_device_usage_device_id_abcd2738 ON public.mobile_device_usage USING btree (device_id);


--
-- TOC entry 3621 (class 1259 OID 67260)
-- Name: mobile_device_usage_device_id_abcd2738_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mobile_device_usage_device_id_abcd2738_like ON public.mobile_device_usage USING btree (device_id varchar_pattern_ops);


--
-- TOC entry 3817 (class 1259 OID 67807)
-- Name: music_created_88f77f_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_created_88f77f_idx ON public.music USING btree (created_at);


--
-- TOC entry 3818 (class 1259 OID 67821)
-- Name: music_created_by_787541fa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_created_by_787541fa ON public.music USING btree (created_by);


--
-- TOC entry 3819 (class 1259 OID 67806)
-- Name: music_genre_148897_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_genre_148897_idx ON public.music USING btree (genre);


--
-- TOC entry 3820 (class 1259 OID 67805)
-- Name: music_is_acti_040a4a_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_is_acti_040a4a_idx ON public.music USING btree (is_active);


--
-- TOC entry 3824 (class 1259 OID 67808)
-- Name: music_plays_music_i_a83db1_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_plays_music_i_a83db1_idx ON public.music_plays USING btree (music_id);


--
-- TOC entry 3825 (class 1259 OID 67833)
-- Name: music_plays_music_id_434243a8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_plays_music_id_434243a8 ON public.music_plays USING btree (music_id);


--
-- TOC entry 3828 (class 1259 OID 67810)
-- Name: music_plays_played__8346ff_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_plays_played__8346ff_idx ON public.music_plays USING btree (played_at);


--
-- TOC entry 3829 (class 1259 OID 67809)
-- Name: music_plays_user_id_4711ae_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_plays_user_id_4711ae_idx ON public.music_plays USING btree (user_id);


--
-- TOC entry 3830 (class 1259 OID 67834)
-- Name: music_plays_user_id_f5589ee3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_plays_user_id_f5589ee3 ON public.music_plays USING btree (user_id);


--
-- TOC entry 3823 (class 1259 OID 67822)
-- Name: music_updated_by_6e6f49a5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX music_updated_by_6e6f49a5 ON public.music USING btree (updated_by);


--
-- TOC entry 3656 (class 1259 OID 67345)
-- Name: operational_sort_or_617ed2_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX operational_sort_or_617ed2_idx ON public.operational_statuses USING btree (sort_order);


--
-- TOC entry 3657 (class 1259 OID 67344)
-- Name: operational_status__0bbf1d_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX operational_status__0bbf1d_idx ON public.operational_statuses USING btree (status_name);


--
-- TOC entry 3660 (class 1259 OID 67343)
-- Name: operational_statuses_status_name_acac0c8e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX operational_statuses_status_name_acac0c8e_like ON public.operational_statuses USING btree (status_name varchar_pattern_ops);


--
-- TOC entry 3665 (class 1259 OID 67347)
-- Name: owner_types_type_na_c589c3_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX owner_types_type_na_c589c3_idx ON public.owner_types USING btree (type_name);


--
-- TOC entry 3666 (class 1259 OID 67346)
-- Name: owner_types_type_name_d3393f45_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX owner_types_type_name_d3393f45_like ON public.owner_types USING btree (type_name varchar_pattern_ops);


--
-- TOC entry 3533 (class 1259 OID 67105)
-- Name: permissions_permission_name_6ba3c52f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX permissions_permission_name_6ba3c52f_like ON public.permissions USING btree (permission_name varchar_pattern_ops);


--
-- TOC entry 3584 (class 1259 OID 67176)
-- Name: role_permissions_granted_by_af5d4915; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX role_permissions_granted_by_af5d4915 ON public.role_permissions USING btree (granted_by);


--
-- TOC entry 3585 (class 1259 OID 67177)
-- Name: role_permissions_permission_id_ad343843; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX role_permissions_permission_id_ad343843 ON public.role_permissions USING btree (permission_id);


--
-- TOC entry 3588 (class 1259 OID 67178)
-- Name: role_permissions_role_id_216516f2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX role_permissions_role_id_216516f2 ON public.role_permissions USING btree (role_id);


--
-- TOC entry 3669 (class 1259 OID 67349)
-- Name: service_cat_categor_322cb1_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX service_cat_categor_322cb1_idx ON public.service_categories USING btree (category_name);


--
-- TOC entry 3670 (class 1259 OID 67348)
-- Name: service_categories_category_name_e069a484_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX service_categories_category_name_e069a484_like ON public.service_categories USING btree (category_name varchar_pattern_ops);


--
-- TOC entry 3591 (class 1259 OID 67196)
-- Name: user_role_assignments_assigned_by_3ab02012; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_role_assignments_assigned_by_3ab02012 ON public.user_role_assignments USING btree (assigned_by);


--
-- TOC entry 3594 (class 1259 OID 67197)
-- Name: user_role_assignments_role_id_4e666b0f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_role_assignments_role_id_4e666b0f ON public.user_role_assignments USING btree (role_id);


--
-- TOC entry 3595 (class 1259 OID 67198)
-- Name: user_role_assignments_user_id_00c0f924; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_role_assignments_user_id_00c0f924 ON public.user_role_assignments USING btree (user_id);


--
-- TOC entry 3540 (class 1259 OID 67106)
-- Name: user_roles_role_name_1bf67ad3_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_roles_role_name_1bf67ad3_like ON public.user_roles USING btree (role_name varchar_pattern_ops);


--
-- TOC entry 3598 (class 1259 OID 67208)
-- Name: user_sessio_expires_66ae96_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_sessio_expires_66ae96_idx ON public.user_sessions USING btree (expires_at);


--
-- TOC entry 3599 (class 1259 OID 67207)
-- Name: user_sessio_is_acti_1b3cb1_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_sessio_is_acti_1b3cb1_idx ON public.user_sessions USING btree (is_active);


--
-- TOC entry 3600 (class 1259 OID 67206)
-- Name: user_sessio_user_id_eb20aa_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_sessio_user_id_eb20aa_idx ON public.user_sessions USING btree (user_id);


--
-- TOC entry 3603 (class 1259 OID 67204)
-- Name: user_sessions_session_id_b4ebe5e4_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_sessions_session_id_b4ebe5e4_like ON public.user_sessions USING btree (session_id varchar_pattern_ops);


--
-- TOC entry 3604 (class 1259 OID 67205)
-- Name: user_sessions_user_id_43ce9642; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX user_sessions_user_id_43ce9642 ON public.user_sessions USING btree (user_id);


--
-- TOC entry 3543 (class 1259 OID 67107)
-- Name: users_email_0ea73cca_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_email_0ea73cca_like ON public.users USING btree (email varchar_pattern_ops);


--
-- TOC entry 3554 (class 1259 OID 67123)
-- Name: users_groups_group_id_2f3517aa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_groups_group_id_2f3517aa ON public.users_groups USING btree (group_id);


--
-- TOC entry 3557 (class 1259 OID 67122)
-- Name: users_groups_user_id_f500bee5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_groups_user_id_f500bee5 ON public.users_groups USING btree (user_id);


--
-- TOC entry 3546 (class 1259 OID 67108)
-- Name: users_phone_number_b4cde146_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_phone_number_b4cde146_like ON public.users USING btree (phone_number varchar_pattern_ops);


--
-- TOC entry 3560 (class 1259 OID 67137)
-- Name: users_user_permissions_permission_id_6d08dcd2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_user_permissions_permission_id_6d08dcd2 ON public.users_user_permissions USING btree (permission_id);


--
-- TOC entry 3563 (class 1259 OID 67136)
-- Name: users_user_permissions_user_id_92473840; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_user_permissions_user_id_92473840 ON public.users_user_permissions USING btree (user_id);


--
-- TOC entry 3551 (class 1259 OID 67109)
-- Name: users_username_e8658fc8_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_username_e8658fc8_like ON public.users USING btree (username varchar_pattern_ops);


--
-- TOC entry 3691 (class 1259 OID 67377)
-- Name: wards_constit_b3144c_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX wards_constit_b3144c_idx ON public.wards USING btree (constituency_id);


--
-- TOC entry 3692 (class 1259 OID 67396)
-- Name: wards_constituency_id_0d753ebe; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX wards_constituency_id_0d753ebe ON public.wards USING btree (constituency_id);


--
-- TOC entry 3695 (class 1259 OID 67379)
-- Name: wards_ward_co_61edb7_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX wards_ward_co_61edb7_idx ON public.wards USING btree (ward_code);


--
-- TOC entry 3696 (class 1259 OID 67395)
-- Name: wards_ward_code_164705e5_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX wards_ward_code_164705e5_like ON public.wards USING btree (ward_code varchar_pattern_ops);


--
-- TOC entry 3699 (class 1259 OID 67378)
-- Name: wards_ward_na_8e1694_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX wards_ward_na_8e1694_idx ON public.wards USING btree (ward_name);


--
-- TOC entry 3844 (class 2606 OID 67149)
-- Name: api_tokens api_tokens_user_id_2db24e1c_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_tokens
    ADD CONSTRAINT api_tokens_user_id_2db24e1c_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3880 (class 2606 OID 67611)
-- Name: audit_trail audit_trail_session_id_43235492_fk_user_sessions_session_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trail
    ADD CONSTRAINT audit_trail_session_id_43235492_fk_user_sessions_session_id FOREIGN KEY (session_id) REFERENCES public.user_sessions(session_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3836 (class 2606 OID 67009)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3837 (class 2606 OID 67004)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3835 (class 2606 OID 66995)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3883 (class 2606 OID 67648)
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3855 (class 2606 OID 67383)
-- Name: constituencies constituencies_county_id_308f52ae_fk_counties_county_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.constituencies
    ADD CONSTRAINT constituencies_county_id_308f52ae_fk_counties_county_id FOREIGN KEY (county_id) REFERENCES public.counties(county_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3881 (class 2606 OID 67618)
-- Name: contact_interactions contact_interactions_contact_id_f5f4544a_fk_facility_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contact_interactions
    ADD CONSTRAINT contact_interactions_contact_id_f5f4544a_fk_facility_ FOREIGN KEY (contact_id) REFERENCES public.facility_contacts(contact_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3882 (class 2606 OID 67631)
-- Name: contact_interactions contact_interactions_device_id_aedd942e_fk_mobile_de; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contact_interactions
    ADD CONSTRAINT contact_interactions_device_id_aedd942e_fk_mobile_de FOREIGN KEY (device_id) REFERENCES public.mobile_device_sessions(device_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3842 (class 2606 OID 67138)
-- Name: custom_tokens custom_tokens_user_id_57e20417_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.custom_tokens
    ADD CONSTRAINT custom_tokens_user_id_57e20417_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3852 (class 2606 OID 67218)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3853 (class 2606 OID 67223)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3892 (class 2606 OID 67751)
-- Name: documents documents_document_type_id_44d85642_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_document_type_id_44d85642_fk_document_ FOREIGN KEY (document_type_id) REFERENCES public.document_types(document_type_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3893 (class 2606 OID 67756)
-- Name: documents documents_gbv_category_c51e0c9d_fk_gbv_categ; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_gbv_category_c51e0c9d_fk_gbv_categ FOREIGN KEY (gbv_category) REFERENCES public.gbv_categories(gbv_category_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3894 (class 2606 OID 67761)
-- Name: documents documents_uploaded_by_fa4ffa51_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_uploaded_by_fa4ffa51_fk_users_user_id FOREIGN KEY (uploaded_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3884 (class 2606 OID 67694)
-- Name: emergency_chat_conversations emergency_chat_conve_assigned_admin_id_c2c47763_fk_users_use; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_conversations
    ADD CONSTRAINT emergency_chat_conve_assigned_admin_id_c2c47763_fk_users_use FOREIGN KEY (assigned_admin_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3885 (class 2606 OID 67699)
-- Name: emergency_chat_conversations emergency_chat_conve_last_message_by_id_72260c9b_fk_users_use; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_conversations
    ADD CONSTRAINT emergency_chat_conve_last_message_by_id_72260c9b_fk_users_use FOREIGN KEY (last_message_by_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3886 (class 2606 OID 67704)
-- Name: emergency_chat_conversations emergency_chat_conve_mobile_session_id_58959a4d_fk_mobile_de; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_conversations
    ADD CONSTRAINT emergency_chat_conve_mobile_session_id_58959a4d_fk_mobile_de FOREIGN KEY (mobile_session_id) REFERENCES public.mobile_device_sessions(device_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3887 (class 2606 OID 67713)
-- Name: emergency_chat_messages emergency_chat_messa_conversation_id_4702a48a_fk_emergency; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_messages
    ADD CONSTRAINT emergency_chat_messa_conversation_id_4702a48a_fk_emergency FOREIGN KEY (conversation_id) REFERENCES public.emergency_chat_conversations(conversation_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3888 (class 2606 OID 67718)
-- Name: emergency_chat_messages emergency_chat_messages_sender_id_3f59dcfd_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_messages
    ADD CONSTRAINT emergency_chat_messages_sender_id_3f59dcfd_fk_users_user_id FOREIGN KEY (sender_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3889 (class 2606 OID 67730)
-- Name: emergency_chat_notifications emergency_chat_notif_conversation_id_ddf27239_fk_emergency; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_notifications
    ADD CONSTRAINT emergency_chat_notif_conversation_id_ddf27239_fk_emergency FOREIGN KEY (conversation_id) REFERENCES public.emergency_chat_conversations(conversation_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3890 (class 2606 OID 67735)
-- Name: emergency_chat_notifications emergency_chat_notif_message_id_d4d8bfe6_fk_emergency; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_notifications
    ADD CONSTRAINT emergency_chat_notif_message_id_d4d8bfe6_fk_emergency FOREIGN KEY (message_id) REFERENCES public.emergency_chat_messages(message_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3891 (class 2606 OID 67725)
-- Name: emergency_chat_notifications emergency_chat_notifications_user_id_c5187218_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_chat_notifications
    ADD CONSTRAINT emergency_chat_notifications_user_id_c5187218_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3857 (class 2606 OID 67469)
-- Name: facilities facilities_created_by_522b765d_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_created_by_522b765d_fk_users_user_id FOREIGN KEY (created_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3858 (class 2606 OID 67474)
-- Name: facilities facilities_operational_status_i_946bd007_fk_operation; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_operational_status_i_946bd007_fk_operation FOREIGN KEY (operational_status_id) REFERENCES public.operational_statuses(operational_status_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3859 (class 2606 OID 67479)
-- Name: facilities facilities_updated_by_c7d06497_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_updated_by_c7d06497_fk_users_user_id FOREIGN KEY (updated_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3860 (class 2606 OID 67484)
-- Name: facilities facilities_ward_id_b19cbd31_fk_wards_ward_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_ward_id_b19cbd31_fk_wards_ward_id FOREIGN KEY (ward_id) REFERENCES public.wards(ward_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3861 (class 2606 OID 67495)
-- Name: facility_contacts facility_contacts_contact_type_id_5380d0c8_fk_contact_t; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_contacts
    ADD CONSTRAINT facility_contacts_contact_type_id_5380d0c8_fk_contact_t FOREIGN KEY (contact_type_id) REFERENCES public.contact_types(contact_type_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3862 (class 2606 OID 67500)
-- Name: facility_contacts facility_contacts_created_by_a5f8561c_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_contacts
    ADD CONSTRAINT facility_contacts_created_by_a5f8561c_fk_users_user_id FOREIGN KEY (created_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3863 (class 2606 OID 67505)
-- Name: facility_contacts facility_contacts_facility_id_c91b40ee_fk_facilitie; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_contacts
    ADD CONSTRAINT facility_contacts_facility_id_c91b40ee_fk_facilitie FOREIGN KEY (facility_id) REFERENCES public.facilities(facility_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3864 (class 2606 OID 67510)
-- Name: facility_contacts facility_contacts_updated_by_f3e4a7e0_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_contacts
    ADD CONSTRAINT facility_contacts_updated_by_f3e4a7e0_fk_users_user_id FOREIGN KEY (updated_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3865 (class 2606 OID 67519)
-- Name: facility_coordinates facility_coordinates_facility_id_d2e67c35_fk_facilitie; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_coordinates
    ADD CONSTRAINT facility_coordinates_facility_id_d2e67c35_fk_facilitie FOREIGN KEY (facility_id) REFERENCES public.facilities(facility_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3866 (class 2606 OID 67530)
-- Name: facility_gbv_categories facility_gbv_categor_facility_id_0cf99a99_fk_facilitie; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_gbv_categories
    ADD CONSTRAINT facility_gbv_categor_facility_id_0cf99a99_fk_facilitie FOREIGN KEY (facility_id) REFERENCES public.facilities(facility_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3867 (class 2606 OID 67535)
-- Name: facility_gbv_categories facility_gbv_categor_gbv_category_id_3b6325a7_fk_gbv_categ; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_gbv_categories
    ADD CONSTRAINT facility_gbv_categor_gbv_category_id_3b6325a7_fk_gbv_categ FOREIGN KEY (gbv_category_id) REFERENCES public.gbv_categories(gbv_category_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3868 (class 2606 OID 67525)
-- Name: facility_gbv_categories facility_gbv_categories_created_by_b61c6e4f_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_gbv_categories
    ADD CONSTRAINT facility_gbv_categories_created_by_b61c6e4f_fk_users_user_id FOREIGN KEY (created_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3869 (class 2606 OID 67543)
-- Name: facility_infrastructure facility_infrastruct_condition_status_id_382dd3f9_fk_condition; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_infrastructure
    ADD CONSTRAINT facility_infrastruct_condition_status_id_382dd3f9_fk_condition FOREIGN KEY (condition_status_id) REFERENCES public.condition_statuses(condition_status_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3870 (class 2606 OID 67548)
-- Name: facility_infrastructure facility_infrastruct_facility_id_42b8797f_fk_facilitie; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_infrastructure
    ADD CONSTRAINT facility_infrastruct_facility_id_42b8797f_fk_facilitie FOREIGN KEY (facility_id) REFERENCES public.facilities(facility_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3871 (class 2606 OID 67553)
-- Name: facility_infrastructure facility_infrastruct_infrastructure_type__c1c3a8d3_fk_infrastru; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_infrastructure
    ADD CONSTRAINT facility_infrastruct_infrastructure_type__c1c3a8d3_fk_infrastru FOREIGN KEY (infrastructure_type_id) REFERENCES public.infrastructure_types(infrastructure_type_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3872 (class 2606 OID 67775)
-- Name: facility_infrastructure facility_infrastructure_created_by_003846c8_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_infrastructure
    ADD CONSTRAINT facility_infrastructure_created_by_003846c8_fk_users_user_id FOREIGN KEY (created_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3873 (class 2606 OID 67781)
-- Name: facility_infrastructure facility_infrastructure_updated_by_91040b96_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_infrastructure
    ADD CONSTRAINT facility_infrastructure_updated_by_91040b96_fk_users_user_id FOREIGN KEY (updated_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3874 (class 2606 OID 67561)
-- Name: facility_owners facility_owners_created_by_6c9f6f73_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_owners
    ADD CONSTRAINT facility_owners_created_by_6c9f6f73_fk_users_user_id FOREIGN KEY (created_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3875 (class 2606 OID 67566)
-- Name: facility_owners facility_owners_facility_id_36e99bf4_fk_facilities_facility_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_owners
    ADD CONSTRAINT facility_owners_facility_id_36e99bf4_fk_facilities_facility_id FOREIGN KEY (facility_id) REFERENCES public.facilities(facility_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3876 (class 2606 OID 67571)
-- Name: facility_owners facility_owners_owner_type_id_7dea0d2c_fk_owner_typ; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_owners
    ADD CONSTRAINT facility_owners_owner_type_id_7dea0d2c_fk_owner_typ FOREIGN KEY (owner_type_id) REFERENCES public.owner_types(owner_type_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3877 (class 2606 OID 67576)
-- Name: facility_owners facility_owners_updated_by_dc292e4e_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_owners
    ADD CONSTRAINT facility_owners_updated_by_dc292e4e_fk_users_user_id FOREIGN KEY (updated_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3878 (class 2606 OID 67585)
-- Name: facility_services facility_services_facility_id_9e5f55dc_fk_facilitie; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_services
    ADD CONSTRAINT facility_services_facility_id_9e5f55dc_fk_facilitie FOREIGN KEY (facility_id) REFERENCES public.facilities(facility_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3879 (class 2606 OID 67590)
-- Name: facility_services facility_services_service_category_id_0c249fbd_fk_service_c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facility_services
    ADD CONSTRAINT facility_services_service_category_id_0c249fbd_fk_service_c FOREIGN KEY (service_category_id) REFERENCES public.service_categories(service_category_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3854 (class 2606 OID 67254)
-- Name: mobile_device_usage mobile_device_usage_device_id_abcd2738_fk_mobile_de; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mobile_device_usage
    ADD CONSTRAINT mobile_device_usage_device_id_abcd2738_fk_mobile_de FOREIGN KEY (device_id) REFERENCES public.mobile_device_sessions(device_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3895 (class 2606 OID 67835)
-- Name: music music_created_by_787541fa_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.music
    ADD CONSTRAINT music_created_by_787541fa_fk_users_user_id FOREIGN KEY (created_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3897 (class 2606 OID 67823)
-- Name: music_plays music_plays_music_id_434243a8_fk_music_music_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.music_plays
    ADD CONSTRAINT music_plays_music_id_434243a8_fk_music_music_id FOREIGN KEY (music_id) REFERENCES public.music(music_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3898 (class 2606 OID 67828)
-- Name: music_plays music_plays_user_id_f5589ee3_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.music_plays
    ADD CONSTRAINT music_plays_user_id_f5589ee3_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3896 (class 2606 OID 67816)
-- Name: music music_updated_by_6e6f49a5_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.music
    ADD CONSTRAINT music_updated_by_6e6f49a5_fk_users_user_id FOREIGN KEY (updated_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3845 (class 2606 OID 67161)
-- Name: role_permissions role_permissions_granted_by_af5d4915_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_granted_by_af5d4915_fk_users_user_id FOREIGN KEY (granted_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3846 (class 2606 OID 67166)
-- Name: role_permissions role_permissions_permission_id_ad343843_fk_permissio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_ad343843_fk_permissio FOREIGN KEY (permission_id) REFERENCES public.permissions(permission_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3847 (class 2606 OID 67171)
-- Name: role_permissions role_permissions_role_id_216516f2_fk_user_roles_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_216516f2_fk_user_roles_role_id FOREIGN KEY (role_id) REFERENCES public.user_roles(role_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3843 (class 2606 OID 67144)
-- Name: user_profiles user_profiles_user_id_8c5ab5fe_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_8c5ab5fe_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3848 (class 2606 OID 67181)
-- Name: user_role_assignments user_role_assignments_assigned_by_3ab02012_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_role_assignments
    ADD CONSTRAINT user_role_assignments_assigned_by_3ab02012_fk_users_user_id FOREIGN KEY (assigned_by) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3849 (class 2606 OID 67186)
-- Name: user_role_assignments user_role_assignments_role_id_4e666b0f_fk_user_roles_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_role_assignments
    ADD CONSTRAINT user_role_assignments_role_id_4e666b0f_fk_user_roles_role_id FOREIGN KEY (role_id) REFERENCES public.user_roles(role_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3850 (class 2606 OID 67191)
-- Name: user_role_assignments user_role_assignments_user_id_00c0f924_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_role_assignments
    ADD CONSTRAINT user_role_assignments_user_id_00c0f924_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3851 (class 2606 OID 67199)
-- Name: user_sessions user_sessions_user_id_43ce9642_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_user_id_43ce9642_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3838 (class 2606 OID 67117)
-- Name: users_groups users_groups_group_id_2f3517aa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3839 (class 2606 OID 67112)
-- Name: users_groups users_groups_user_id_f500bee5_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_f500bee5_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3840 (class 2606 OID 67131)
-- Name: users_user_permissions users_user_permissio_permission_id_6d08dcd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3841 (class 2606 OID 67126)
-- Name: users_user_permissions users_user_permissions_user_id_92473840_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_92473840_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3856 (class 2606 OID 67390)
-- Name: wards wards_constituency_id_0d753ebe_fk_constitue; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wards
    ADD CONSTRAINT wards_constituency_id_0d753ebe_fk_constitue FOREIGN KEY (constituency_id) REFERENCES public.constituencies(constituency_id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2025-09-03 11:52:19 EAT

--
-- PostgreSQL database dump complete
--

